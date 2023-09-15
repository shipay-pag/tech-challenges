from fastapi import APIRouter, Depends, FastAPI, Request
from dependency_injector.wiring import inject, Provide

from infrastructure.containers import Container
from endpoints.registration.manager import Orchestrator

router = APIRouter()


@router.get('/registration/customers')
@inject
async def get_customers(request: Request, orchestrator: Orchestrator = Depends(Provide[Container.registration_service]),):
    customer_id = request.path_params['identity'].get('customer_id')
    return await orchestrator.find_customer_by_id(customer_id=customer_id)


def configure(app: FastAPI):
    app.include_router(router)
