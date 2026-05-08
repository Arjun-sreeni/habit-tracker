from datetime import date
from sqlalchemy.orm import Session
from app.models import HabitLog, Habit
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError


def log_habit(db: Session, habit_id: int, user_id: int, log_date: date) -> dict | None:
    stmt = select(Habit).where(Habit.id == habit_id, Habit.user_id == user_id)
    habit = db.execute(stmt).scalar_one_or_none()
    if not habit:
        return None

    stmt = select(HabitLog).where(
        HabitLog.habit_id == habit_id, HabitLog.log_date == log_date
    )
    existing_log = db.execute(stmt).scalar_one_or_none()

    if existing_log:
        return {"created": False, "log": existing_log}

    new_log = HabitLog(log_date=log_date, habit_id=habit_id)
    try:
        db.add(new_log)
        db.commit()
        db.refresh(new_log)
        return {"created": True, "log": new_log}

    except IntegrityError:
        db.rollback()
        stmt = select(HabitLog).where(
            HabitLog.habit_id == habit_id, HabitLog.log_date == log_date
        )
        existing_habit_log = db.execute(stmt).scalar_one_or_none()
        if existing_habit_log:
            return {"created": False, "log": existing_habit_log}
        raise
