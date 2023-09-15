import traceback

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            return await call_next(request)
        except Exception as exception:
            trace = ''.join(traceback.format_exception(etype=type(exception), value=exception, tb=exception.__traceback__))
            content_error = f'Exception: {exception} - StackTrace: {trace}'
            return JSONResponse(status_code=500, content=content_error)
