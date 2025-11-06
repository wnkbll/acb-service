import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from src.api.routes import router
from src.core.paths import LOGGING_DIR
from src.core.settings import Settings, get_app_settings


@asynccontextmanager
async def lifespan(_: FastAPI):
    yield


def get_application() -> FastAPI:
    settings: Settings = get_app_settings()

    logger.configure(
        handlers=[  # type: ignore
            dict(
                sink=LOGGING_DIR.joinpath(settings.logging.file),
                level="WARNING",
                rotation=settings.logging.rotation,
                compression=settings.logging.compression,
                serialize=True,
            ),
            dict(
                sink=sys.stderr,
                level="TRACE",
            ),
        ],
    )

    application: FastAPI = FastAPI(**settings.fastapi_kwargs, lifespan=lifespan)

    application.include_router(router, prefix="/api")

    application.add_middleware(
        CORSMiddleware,
        **settings.middleware_kwargs,
    )

    return application


app: FastAPI = get_application()
