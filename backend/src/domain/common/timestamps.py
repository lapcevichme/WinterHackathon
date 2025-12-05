from datetime import datetime
from pydantic import BaseModel, Field


class CreatedAtModel(BaseModel):
    created_at: datetime = Field(...)

class TimestampModel(CreatedAtModel):
    updated_at: datetime | None = Field(None)
