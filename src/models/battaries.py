from datetime import date
from pydantic import BaseModel

from src.models import TimestampsModelMixin

class BatteryResponseModel(TimestampsModelMixin):
    id: int
    device_id: int
    name: str
    voltage: int
    capacity: int
    validity_period: date
