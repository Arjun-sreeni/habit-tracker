import enum
from datetime import datetime
from sqlalchemy import Integer, String, DateTime, func, Enum, Boolean, false, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class FrequencyTypes(str, enum.Enum):
    daily = "daily"
    weekly = "weekly"
    custom = "custom"


class Habit(Base):
    __tablename__ = "habits"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    frequency: Mapped[FrequencyTypes] = mapped_column(
        Enum(FrequencyTypes), nullable=False
    )
    is_archived: Mapped[bool] = mapped_column(
        Boolean, server_default=false(), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
