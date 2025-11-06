from fastapi import APIRouter

from src.api.dependencies import BindServiceDepends
from src.models import SuccessMessage
from src.models.bind import BindManyCreateModel, BindOneCreateModel

router = APIRouter()


@router.post(
    "/many",
    summary="Создать связь между устройством и аккумуляторами",
    response_model=SuccessMessage,
)
async def create_binds(
    bind: BindManyCreateModel, service: BindServiceDepends
) -> SuccessMessage:
    return await service.bind_many(bind)


@router.post(
    "/one",
    summary="Создать связь между устройством и аккумулятором",
    response_model=SuccessMessage,
)
async def create_bind(
    bind: BindOneCreateModel, service: BindServiceDepends
) -> SuccessMessage:
    return await service.bind_one(bind)


@router.delete(
    "/{battery_id}",
    summary="Удалить связь аккумулятора с устройством",
    response_model=SuccessMessage,
)
async def delete_bind(battery_id: int, service: BindServiceDepends) -> SuccessMessage:
    return await service.delete_bind(battery_id)
