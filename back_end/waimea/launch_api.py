from uuid import uuid4
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, FastAPI, HTTPException, Request
from shipay_auth_async.interfaces import AuthAdapter
from shipay.infrastructure.containers import Container
from shipay.endpoints.schemas import LaunchRequestBody
from shipay.launch.rules import RulesEngine
from shipay.services import LaunchService

router = APIRouter()
auth_client = shipay_auth_async.client()

@router.post('/v1/rocket/launch', tags=['rocket'])
@inject
@auth_client.required_authenticator([AuthAdapter(Container.claims_service(),
                                                 route='/v1/rocket/launch/post',
                                                 type_filter='resource'),
                                     AuthAdapter(Container.jwt_service())])
async def launch(request: Request, schema: LaunchRequestBody = None,
                 service: LaunchService = Depends(Provide[Container.launch_service])):
    try:
        trace_id = request.headers.get('trace_id', str(uuid4()))
        if not schema:
            raise HTTPException(status_code=400, detail='where is the request payload?')
        
        if not RulesEngine.is_launch_approved(schema):
            raise HTTPException(status_code=405, detail='your launch is not allowed.')
            
        pre_flight = await service.pre_flight_check()
        
        if not RulesEngine.is_pre_flight_status_equals_ok(pre_flight.status):
            raise HTTPException(status_code=500, detail='your launch is compromised, please abort.')
        
        countdown_status = service.countdown()

        return await service.launch(trace_id=trace_id,
                                    customer_id=schema.customer_id,
                                    countdown_status=countdown_status,
                                    pre_flight=pre_flight)

    except Exception as exception:
        raise HTTPException(status_code=500, detail=f'Error during launch...{exception.args[0]}')