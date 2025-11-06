from datetime import datetime
from pydantic import BaseModel


class TimestampsModelMixin(BaseModel):
    created_at: datetime
    updated_at: datetime
