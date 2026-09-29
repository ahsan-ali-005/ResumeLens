from fastapi import Request
from datetime import datetime
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.dependencies import create_log
import time


class RequestTimeMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        start = time.perf_counter()
        response = await call_next(request)
        time_taken = round(time.perf_counter() - start, 4)
        now = datetime.now()

        create_log(
            date=now.date(),
            time=now.strftime("%H:%M:%S"),
            method=request.method,
            status=response.status_code,
            time_taken=time_taken,
            endpoint=request.url.path
        )
        return response