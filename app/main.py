from fastapi import FastAPI
from app.routers import health, auth, habits
from app.config import settings

app = FastAPI(title=settings.app_name, debug=settings.debug)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(habits.router)
