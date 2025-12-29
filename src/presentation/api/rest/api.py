from fastapi import APIRouter
from src.presentation.api.rest.v1.router import router as v1_router


api_router = APIRouter()

# v1 — основная текущая версия
api_router.include_router(v1_router, prefix="/api/v1")

# Опционально: /api/latest → то же, что и v1 (удобно для фронтенда)
api_router.include_router(v1_router, prefix="/api/latest")
