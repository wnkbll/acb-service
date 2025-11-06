from typing import Callable, Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from src.core.settings import get_app_settings
from src.core.settings import Settings
from src.db.postgres import Postgres
from src.db.repositories.repository import Repository
from src.db.repositories.battaries import BattariesRepository
from src.db.repositories.devices import DevicesRepository


def get_async_session_factory():
    async_engine: AsyncEngine = Postgres.get_async_engine() # type: ignore

    async_session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
        bind=async_engine, autoflush=False, expire_on_commit=False
    )

    return async_session_factory


def get_repository(repository: type[Repository]) -> Callable[[async_sessionmaker[AsyncSession]], Repository]:
    def __get_repo(
            async_session_factory: async_sessionmaker[AsyncSession] = Depends(get_async_session_factory)
    ) -> Repository:
        return repository(async_session_factory)

    return __get_repo


BattariesRepositoryDepends = Annotated[BattariesRepository, Depends(get_repository(BattariesRepository))]
DevicesRepositoryDepends = Annotated[DevicesRepository, Depends(get_repository(DevicesRepository))]

SettingsDepends = Annotated[Settings, Depends(get_app_settings)]
