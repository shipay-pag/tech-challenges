import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from infrastructure.containers import Container
from middlewares.exception_handler import ExceptionHandlerMiddleware


def create_app() -> FastAPI:
    app = FastAPI(openapi_url='/default_spec')
    container = Container()

    from endpoints.health import controllers as health_module
    health_module.configure(app)

    container.wire(modules=[health_module])

    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"],
                       allow_headers=["*"])
    app.add_middleware(ExceptionHandlerMiddleware)

    app.container = container
    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
