from fastapi import APIRouter, Depends, HTTPException
from app.schemas.habit import HabitCreate, HabitUpdate, HabitResponse
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.database import get_db
from sqlalchemy.orm import Session
from app.services.habit import (
    create_habit as create_habit_service,
    get_user_habits,
    get_habit_by_id as get_habit_by_id_service,
    update_habit as update_habit_service,
    delete_habit as delete_habit_service,
)

router = APIRouter(prefix="/habits", tags=["Habit"])


@router.post("/", status_code=201, response_model=HabitResponse)
def create_habit(
    habit_data: HabitCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_id = user.id
    created_habit = create_habit_service(db, user_id, habit_data)
    return created_habit


@router.get("/", response_model=list[HabitResponse])
def get_habit(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    user_id = user.id
    user_habits = get_user_habits(db, user_id)
    return user_habits


@router.get("/{habit_id}", response_model=HabitResponse)
def get_habit_by_id(
    habit_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    user_id = user.id
    habit = get_habit_by_id_service(db, user_id, habit_id)
    if habit is None:
        raise HTTPException(status_code=404, detail="habit not found")
    return habit


@router.patch("/{habit_id}", response_model=HabitResponse)
def update_habit(
    habit_id: int,
    update_date: HabitUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    user_id = user.id
    updated_habit = update_habit_service(db, habit_id, user_id, update_date)
    if updated_habit is None:
        raise HTTPException(status_code=404, detail="habit not found")
    return updated_habit


@router.delete("/{habit_id}", status_code=204)
def delete_habit(
    habit_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    user_id = user.id
    result = delete_habit_service(db, habit_id, user_id)
    if not result:
        raise HTTPException(status_code=404, detail="habit not found")
