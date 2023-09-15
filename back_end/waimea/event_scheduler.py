from rq import Queue
from redis import Redis
from functions import publish_event

from fastapi import APIRouter, HTTPException, Request
from shipay_auth_async.interfaces import AuthAdapter
from shipay.infrastructure.containers import Container
from shipay.endpoints.schemas import RequestBody


router = APIRouter()
auth_client = shipay_auth_async.client()

@router.post('/v1/render/scheduler', tags=['render'])
@auth_client.required_authenticator([AuthAdapter(Container.claims_service(),
                                                 route='/v1/render/scheduler/post',
                                                 type_filter='resource'),
                                     AuthAdapter(Container.jwt_service())])
async def scheduler(request: Request, schema: RequestBody = None):
    try:

        if not schema:
            raise HTTPException(status_code=400, detail='where is the request payload?')
            
        queue = Queue(name='default', connection=Redis())

        return await queue.enqueue_at(schema.scheduler_datetime, publish_event, schema.event_content)

    except Exception as exception:
        raise HTTPException(status_code=500, detail=f'Error during scheduler event...{exception.args[0]}')