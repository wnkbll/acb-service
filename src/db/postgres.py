from loguru import logger
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from src.core.settings import get_app_settings


class Postgres:
    @staticmethod
    def get_async_engine() -> AsyncEngine | None:
        try:
            async_engine: AsyncEngine = create_async_engine(get_app_settings().postgres_dsn)
            return async_engine
        except SQLAlchemyError as e:
            logger.warning("Unable to establish db engine, database might not exist yet")
            logger.warning(e)
