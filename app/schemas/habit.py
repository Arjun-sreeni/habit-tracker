from datetime import datetime
from pydantic import BaseModel, ConfigDict, model_validator
from app.models.habit import FrequencyTypes


class HabitCreate(BaseModel):
    name: str
    frequency: FrequencyTypes
    schedule_days: list[str] | None = None

    @model_validator(mode="after")
    def validate_schedule(self):
        days = {"mon", "tue", "wed", "thu", "fri", "sat", "sun"}
        if self.schedule_days:
            self.schedule_days = [day.lower().strip() for day in self.schedule_days]

        if self.frequency == FrequencyTypes.daily:
            self.schedule_days = list(days)

        elif self.frequency == FrequencyTypes.weekly:
            if not self.schedule_days:
                raise ValueError("weekly habit requires exactly one day")
            if len(self.schedule_days) > 1:
                raise ValueError("weekly habits does not support more than one day")
            if self.schedule_days[0] not in days:
                raise ValueError(f"invalid day{self.schedule_days[0]}, Valid days are, mon, tue, wed, thu, fri, sat, sun")

            
        elif self.frequency == FrequencyTypes.custom:
            if not self.schedule_days:
                raise ValueError("no custom days given")
            if len(self.schedule_days) != len(set(self.schedule_days)):
                raise ValueError("duplicates days dont allowed")
            if not set(self.schedule_days).issubset(days):
                raise ValueError("days must be mon, tue, wed, thu, fri, sat, sun") 
            if len(self.schedule_days) > 6:
                raise ValueError("custom days cannot be more than 6 days")
        return self
        


class HabitResponse(BaseModel):
    id: int
    name: str
    frequency: FrequencyTypes
    schedule_days: list[str] 
    is_archived: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class HabitUpdate(BaseModel):
    name: str | None = None
    frequency: FrequencyTypes | None = None
    is_archived: bool | None = None
    schedule_days: list[str] | None = None
