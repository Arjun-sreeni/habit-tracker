from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import UserCreate, UserResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.auth import create_user

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/register", status_code=201, response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        user = create_user(db, user_data)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    return user