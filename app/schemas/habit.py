from pydantic import BaseModel, ConfigDict
from datetime import datetime


class HabitCreate(BaseModel):
    name: str
    frequency: str


class HabitResponse(BaseModel):
    id: int
    name: str
    frequency: str
    is_archived: bool
    created_at: datetime
