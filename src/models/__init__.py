from datetime import datetime
from typing import Literal

from pydantic import BaseModel

SuccessMessages = Literal[
    "Запись успешно создана", "Запись успешно обновлена", "Запись успешно удалена"
]


class SuccessMessage(BaseModel):
    message: SuccessMessages


class TimestampsModelMixin(BaseModel):
    created_at: datetime
    updated_at: datetime
