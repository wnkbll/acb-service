from datetime import date

from pydantic import BaseModel

from src.models import TimestampsModelMixin


class BatteryResponseModel(TimestampsModelMixin):
    id: int
    device_id: int | None = None
    name: str
    voltage: int
    capacity: int
    validity_period: date


class BatteryCreateModel(BaseModel):
    name: str
    voltage: int
    capacity: int
    validity_period: date


class BatteryUpdateModel(BaseModel):
    name: str | None = None
    voltage: int | None = None
    capacity: int | None = None
    validity_period: date | None = None
