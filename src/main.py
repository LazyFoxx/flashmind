from fastapi import FastAPI

from src.config.settings import settings
from src.presentation.api.rest.api import api_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(api_router)
