from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import UserCreate, UserResponse, UserLogin
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.auth import create_user, authenticate_user
from app.services.jwt import create_access_token, verify_access_token
from app.dependencies.auth import get_current_user
from app.models import User


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

@router.post("/login")
def login(user_login_data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, user_login_data.email, user_login_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="invalid credentials")
    token = create_access_token({
        "sub": str(user.id)
    })
    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
