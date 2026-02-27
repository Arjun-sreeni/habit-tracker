from fastapi import FastAPI
from app.routers.health import router
from app.config import settings

app = FastAPI(title=settings.app_name, debug=settings.debug)

app.include_router(router)


