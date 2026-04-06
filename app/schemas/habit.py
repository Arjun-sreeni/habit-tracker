from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.models.habit import FrequencyTypes


class HabitCreate(BaseModel):
    name: str
    frequency: FrequencyTypes


class HabitResponse(HabitCreate):
    id: int
    is_archived: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class HabitUpdate(BaseModel):
    name: str | None = None
    frequency: FrequencyTypes | None = None
    is_archived: bool | None = None
