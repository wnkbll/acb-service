from fastapi import APIRouter, HTTPException, status

from src.api.dependencies import DevicesServiceDepends
from src.db.errors import EntityDoesNotExistError
from src.models.devices import DeviceCreateModel, DeviceResponseModel

router = APIRouter()


@router.get(
    "/{id_}",
    summary="Получить запись устройства",
    description="Возвращает запись устройства по переданному id",
    response_model=DeviceResponseModel,
)
async def get_device(
    id_: int, device_repo: DevicesServiceDepends
) -> DeviceResponseModel:
    try:
        device = await device_repo.get(id_=id_)
    except EntityDoesNotExistError as existence_error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"There is no device with this id:{id_}",
        ) from existence_error

    return device


@router.get(
    "/",
    summary="Получить записи устройств",
    description="Возвращает записи устройств по переданному id",
    response_model=list[DeviceResponseModel],
)
async def get_devices(device_repo: DevicesServiceDepends) -> list[DeviceResponseModel]:
    return await device_repo.get_all()


@router.post(
    "/",
    summary="Создать запись устройства",
    description="Создает запись устройства",
    response_model=DeviceResponseModel,
)
async def create_device(device: DeviceCreateModel, device_repo: DevicesServiceDepends):
    pass


@router.put(
    "/{id_}",
    summary="Обновить запись устройства",
    description="Обновляет запись устройства по переданному id",
    response_model=DeviceResponseModel,
)
async def update_device(
    id_: int, device_repo: DevicesServiceDepends
) -> DeviceResponseModel:
    try:
        device = await device_repo.get(id_=id_)
    except EntityDoesNotExistError as existence_error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"There is no device with this id:{id_}",
        ) from existence_error

    return device


@router.delete(
    "/{id_}",
    summary="Удалить запись устройства",
    description="Удаляет запись устройства по переданному id",
    response_model=DeviceResponseModel,
)
async def delete_device(
    id_: int, device_repo: DevicesServiceDepends
) -> DeviceResponseModel:
    try:
        device = await device_repo.get(id_=id_)
    except EntityDoesNotExistError as existence_error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"There is no device with this id:{id_}",
        ) from existence_error

    return device
