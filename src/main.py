from fastapi import FastAPI

from src.config.settings import settings
from src.presentation.api.rest.v1.routers.cards import router as cards_router
from src.presentation.api.rest.v1.routers.decks import router as decks_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(cards_router)
app.include_router(decks_router)


# @app.get("/")
# async def root():
#     return {
#         "message": "Hello from FlashMind backend! 🚀",
#         "docs": "Перейди на /docs для интерактивной документации",
#         "version": settings.APP_VERSION,
#     }
