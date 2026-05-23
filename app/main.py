from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.api.v1.router import api_router
from app.core.config import settings
from app.db.client import init_db, close_db
from app.api.middlewares.logging import configure_logging
from app.api.middlewares.logging import LoggingMiddleware


configure_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="User Management API built with FastAPI, and MongoDB",
    lifespan=lifespan,
)


app.add_middleware(LoggingMiddleware)


@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "ok",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
        },
    )


app.include_router(api_router, prefix=settings.API_V1_STR)