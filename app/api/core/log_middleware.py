# app/api/core/middleware.py
import time
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

from .logging_utils import Logger

class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, ignore_paths=None):
        super().__init__(app)
        self.ignore_paths = ignore_paths or ["/docs", "/openapi.json", "/redoc"]

    async def dispatch(self, request: Request, call_next):
        # Ignora paths internos
        if request.url.path in self.ignore_paths:
            return await call_next(request)

        job_id = str(uuid.uuid4())
        logger = Logger(job_id=job_id, config={"path": request.url.path, "method": request.method})
        logger.start()

        # Disponibiliza logger na request
        request.state.logger = logger  

        start_time = time.time()
        try:
            response = await call_next(request)
        except Exception as e:
            logger.log_event("Error", {"error": str(e)})
            raise e
        finally:
            duration = time.time() - start_time
            logger.end({"duration": duration})

        return response
