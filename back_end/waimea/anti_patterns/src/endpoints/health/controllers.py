from fastapi import APIRouter, Depends, FastAPI
from dependency_injector.wiring import inject, Provide
from starlette import status
from starlette.responses import JSONResponse

from infrastructure.containers import Container
from endpoints.health.service import HealthService


router = APIRouter()

@router.get('/beat')
@inject
async def get_beat():
    return JSONResponse(status_code=status.HTTP_200_OK, content="OK")


@router.get('/health')
@inject
async def get_health(health_service: HealthService = Depends(Provide[Container.health_service]),):
    statuses = await health_service.get_health_status()
    if not all(statuses.values()):
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content=statuses)

    return statuses


def configure(app: FastAPI):
    app.include_router(router)
