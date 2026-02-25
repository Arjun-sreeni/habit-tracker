from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.routers.health import router
from app.database import get_db
from app.config import settings

app = FastAPI(title=settings.app_name, debug=settings.debug)

app.include_router(router)


@app.get("/dbcheck")
def db_check(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"db_status": "connected"}
