# tests/conftest.py
from httpx import AsyncClient, ASGITransport
from src.main import app
from pytest_asyncio import fixture


# Базовый клиент для всех тестов
@fixture(scope="module")
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
        follow_redirects=True,
    ) as ac:
        yield ac


# Фиксированный deck_id (или можно генерить uuid4())
@fixture
def sample_deck_id():
    return "550e8400-e29b-41d4-a716-446655440000"


# Создаёт карточку и возвращает её id
@fixture
async def created_card_id(client, sample_deck_id):
    payload = {
        "deck_id": sample_deck_id,
        "front": "Фикстура — это магия pytest",
        "back": "Она готовит данные автоматически",
    }
    response = await client.post("/cards/", json=payload)
    assert response.status_code == 201
    return response.json()["id"]
