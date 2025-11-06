from typing import Annotated, Callable

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from src.core.settings import Settings, get_app_settings
from src.db.postgres import Postgres
from src.services import Service
from src.services.batteries import BatteriesService
from src.services.bind import BindService
from src.services.devices import DevicesService


def get_async_session_factory():
    async_engine: AsyncEngine = Postgres.get_async_engine()  # type: ignore

    async_session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
        bind=async_engine, autoflush=False, expire_on_commit=False
    )

    return async_session_factory


def get_service(
    service: type[Service],
) -> Callable[[async_sessionmaker[AsyncSession]], Service]:
    def __get_repo(
        async_session_factory: async_sessionmaker[AsyncSession] = Depends(
            get_async_session_factory
        ),
    ) -> Service:
        return service(async_session_factory)

    return __get_repo


BatteriesServiceDepends = Annotated[
    BatteriesService, Depends(get_service(BatteriesService))
]
DevicesServiceDepends = Annotated[DevicesService, Depends(get_service(DevicesService))]
BindServiceDepends = Annotated[BindService, Depends(get_service(BindService))]

SettingsDepends = Annotated[Settings, Depends(get_app_settings)]
