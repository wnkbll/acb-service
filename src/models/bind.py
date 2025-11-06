from pydantic import BaseModel


class BindManyCreateModel(BaseModel):
    device_id: int
    batteries: list[int]


class BindOneCreateModel(BaseModel):
    device_id: int
    battery_id: int
