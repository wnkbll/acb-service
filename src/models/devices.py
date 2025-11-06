from pydantic import BaseModel

from src.models import TimestampsModelMixin
from src.models.batteries import BatteryResponseModel


class DeviceResponseModel(TimestampsModelMixin):
    id: int
    name: str
    version: str
    is_active: bool
    batteries: list[BatteryResponseModel]


class DeviceCreateModel(BaseModel):
    name: str
    version: str
    is_active: bool


class DeviceUpdateModel(BaseModel):
    name: str | None = None
    version: str | None = None
    is_active: bool | None = None
