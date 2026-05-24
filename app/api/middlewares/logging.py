import logging
from typing import Callable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp


def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.logger = logging.getLogger("uvicorn.access")

    async def dispatch(self, request: Request, call_next: Callable):
        self.logger.info(f"Request: {request.method} {request.url}")
        response = await call_next(request)
        self.logger.info(
            f"Response: {request.method} {request.url} - {response.status_code}"
        )
        return response