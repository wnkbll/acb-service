from pydantic import BaseModel

from src.models import TimestampsModelMixin
from src.models.battaries import BatteryResponseModel


class DeviceInDB(TimestampsModelMixin):
    id: int
    name: str
    version: str
    is_active: bool


class DeviceResponseModel(DeviceInDB):
    batteries: list[BatteryResponseModel]


class DeviceCreateModel(BaseModel):
    name: str
    version: str
    is_active: bool
    batteries: list[int] | None
