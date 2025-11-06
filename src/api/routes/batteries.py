from fastapi import APIRouter

from src.api.dependencies import BatteriesServiceDepends
from src.models import SuccessMessage
from src.models.batteries import (
    BatteryCreateModel,
    BatteryResponseModel,
    BatteryUpdateModel,
)

router = APIRouter()


@router.get(
    "/{battery_id}",
    summary="Получить запись аккумулятора",
    description="Возвращает запись аккумулятора по переданному id",
    response_model=BatteryResponseModel,
)
async def get_battery(
    battery_id: int, service: BatteriesServiceDepends
) -> BatteryResponseModel:
    return await service.get_battery(battery_id)


@router.get(
    "",
    summary="Получить записи аккумуляторов",
    description="Возвращает список записей аккумуляторов",
    response_model=list[BatteryResponseModel],
)
async def get_batteries(service: BatteriesServiceDepends) -> list[BatteryResponseModel]:
    return await service.get_batteries()


@router.post(
    "",
    summary="Создать запись аккумулятора",
    description="Создает запись аккумулятора",
    response_model=SuccessMessage,
)
async def create_battery(
    battery: BatteryCreateModel, service: BatteriesServiceDepends
) -> SuccessMessage:
    return await service.create_battery(battery)


@router.put(
    "/{battery_id}",
    summary="Обновить запись аккумулятора",
    description="Обновляет запись аккумулятора по переданному id",
    response_model=SuccessMessage,
)
async def update_battery(
    battery_id: int, battery: BatteryUpdateModel, service: BatteriesServiceDepends
) -> SuccessMessage:
    return await service.update_battery(battery_id, battery)


@router.delete(
    "/{battery_id}",
    summary="Удалить запись аккумулятора",
    description="Удаляет запись аккумулятора по переданному id",
    response_model=SuccessMessage,
)
async def delete_battery(
    battery_id: int, service: BatteriesServiceDepends
) -> SuccessMessage:
    return await service.delete_battery(battery_id)
