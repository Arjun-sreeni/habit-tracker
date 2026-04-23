from app.schemas.habit import HabitCreate, HabitUpdate
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models import Habit




# creating habit
def create_habit(db: Session, user_id: int, habit_data: HabitCreate) -> Habit:
    habit = Habit(name=habit_data.name, frequency=habit_data.frequency, user_id=user_id)
    db.add(habit)
    db.commit()
    db.refresh(habit)
    return habit


# getting user habits
def get_user_habits(db: Session, user_id: int) -> list[Habit]:
    stmt = select(Habit).where(Habit.user_id == user_id)
    return list(db.execute(stmt).scalars())

# geting habit by habit id
def get_habit_by_id(db: Session, user_id: int, habit_id: int) -> Habit | None:
    stmt = select(Habit).where(
        Habit.id == habit_id,
        Habit.user_id == user_id
        )
    return db.execute(stmt).scalar_one_or_none()

# updating habit
def update_habit(db: Session, habit_id: int, user_id: int, update_data: HabitUpdate) -> Habit | None:
    stmt = select(Habit).where(
        Habit.id == habit_id,
        Habit.user_id == user_id
    )
    result = db.execute(stmt).scalar_one_or_none()

    if result is None:
        return None

    updated_dict = update_data.model_dump(exclude_unset=True)
    

    for key, value in updated_dict.items():
        setattr(result, key, value)
    try:
        db.commit()
        db.refresh(result)
        return result
    except Exception:
        db.rollback()
        raise 

def delete_habit(db: Session, habit_id: int, user_id: int) -> bool:
    stmt = select(Habit).where(
        Habit.id == habit_id,
        Habit.user_id == user_id
    )

    result = db.execute(stmt).scalar_one_or_none()

    if result is None:
        return False
    

    db.delete(result)
    db.commit()
    return True

