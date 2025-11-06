from datetime import datetime

from pydantic import BaseModel


class SuccessMessage(BaseModel):
    message: str = "Запись успешно создана"


class TimestampsModelMixin(BaseModel):
    created_at: datetime
    updated_at: datetime
