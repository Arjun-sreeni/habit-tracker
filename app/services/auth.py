from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.models import User


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str) -> str:
    return  pwd_context.hash(password)
     


def create_user(db: Session, user_data: UserCreate):
    user = db.query(User).filter(User.email == user_data.email).first()
    if user:
        raise ValueError("Email already exists")
    
    hashed_password = hash_password(user_data.password)
    user = User(email = user_data.email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
