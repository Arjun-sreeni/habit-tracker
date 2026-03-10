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


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db: Session, email: str,  password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
       return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
