from pydantic import BaseModel

from src.models import TimestampsModelMixin
from src.models.battaries import BatteryResponseModel


class DeviceResponseModel(TimestampsModelMixin):
    id: int
    name: str
    version: str
    is_active: bool
    batteries: list[BatteryResponseModel]
