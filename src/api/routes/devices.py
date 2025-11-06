from fastapi import APIRouter

from src.api.dependencies import DevicesServiceDepends
from src.models import SuccessMessage
from src.models.devices import DeviceCreateModel, DeviceResponseModel, DeviceUpdateModel

router = APIRouter()


@router.get(
    "/{device_id}",
    summary="Получить запись устройства",
    description="Возвращает запись устройства по переданному id",
    response_model=DeviceResponseModel,
)
async def get_device(
    device_id: int, service: DevicesServiceDepends
) -> DeviceResponseModel:
    return await service.get(device_id)


@router.get(
    "",
    summary="Получить записи устройств",
    description="Возвращает записи устройств по переданному id",
    response_model=list[DeviceResponseModel],
)
async def get_devices(service: DevicesServiceDepends) -> list[DeviceResponseModel]:
    return await service.get_all()


@router.post(
    "",
    summary="Создать запись устройства",
    description="Создает запись устройства",
    response_model=SuccessMessage,
)
async def create_device(
    device: DeviceCreateModel, service: DevicesServiceDepends
) -> SuccessMessage:
    return await service.create(device)


@router.put(
    "/{device_id}",
    summary="Обновить запись устройства",
    description="Обновляет запись устройства по переданному id",
    response_model=SuccessMessage,
)
async def update_device(
    device_id: int, device: DeviceUpdateModel, service: DevicesServiceDepends
) -> SuccessMessage:
    return await service.update(device_id, device)


@router.delete(
    "/{device_id}",
    summary="Удалить запись устройства",
    description="Удаляет запись устройства по переданному id",
    response_model=SuccessMessage,
)
async def delete_device(
    device_id: int, service: DevicesServiceDepends
) -> SuccessMessage:
    return await service.delete(device_id)
