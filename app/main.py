from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import JSONResponse

from .api.v1.router import api_router
from .core.config import settings
from .db.client import init_db, close_db
from .api.middlewares.logging import configure_logging, LoggingMiddleware


configure_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await init_db()
        print("DB initialized")
    except Exception as e:
        print(f"DB init failed: {e}")

    yield

    await close_db()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="User Management API built with FastAPI, and MongoDB",
    lifespan=lifespan,
)


app.add_middleware(LoggingMiddleware)


@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "ok",
        "service": settings.app_name,
        "version": settings.app_version,
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    if isinstance(exc, HTTPException):
        return await http_exception_handler(request, exc)

    logging.exception("Unhandled exception")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
        },
    )


app.include_router(api_router, prefix=settings.api_v1_str)
