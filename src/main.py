from fastapi import FastAPI

app = FastAPI(
    title="FlashMind",
    version="0.1.0",
    description="Anki-like flashcards backend на FastAPI + Clean/DDD Architecture + Python 3.13",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)


@app.get("/")
async def root():
    return {
        "message": "Hello from FlashMind backend! 🚀",
        "docs": "Перейди на /docs для интерактивной документации",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "flashmind-api"}
