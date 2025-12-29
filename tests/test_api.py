import pytest

# тестирование работоспособности


@pytest.mark.asyncio
async def test_health_check(client):
    response = await client.get("/docs")
    assert response.status_code == 200


# тестирование cards


@pytest.mark.asyncio
async def test_create_card(client, sample_deck_id):
    """Создаем карточку"""

    payload = {
        "deck_id": sample_deck_id,  # uuid
        "front": "Зачем нужны интеграционные тесты?",
        "back": "интеграционные тесты нужны для многих задач писать лень",
    }

    response = await client.post("/cards/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["front"] == payload["front"]
    assert data["back"] == payload["back"]
    assert data["deck_id"] == sample_deck_id


@pytest.mark.asyncio
async def test_get_card_by_id(client, created_card_id):
    """Получаем карточку по ее id"""

    response = await client.get(f"/cards/{created_card_id}")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_update_card(client, created_card_id):
    """Обновление полей карточки"""

    update_payload = {"front": "Обновлённый вопрос", "back": "Обновлённый ответ"}
    response = await client.patch(f"/cards/{created_card_id}", json=update_payload)

    assert response.status_code == 200
    data = response.json()
    assert data["front"] == "Обновлённый вопрос"
    assert data["back"] == "Обновлённый ответ"

    update_payload = {"back": "Обновлённый ответ 2"}
    response = await client.patch(f"/cards/{created_card_id}", json=update_payload)

    assert response.status_code == 200
    data = response.json()
    assert data["front"] == "Обновлённый вопрос"
    assert data["back"] == "Обновлённый ответ 2"


@pytest.mark.asyncio
async def test_delete_card(client, created_card_id):
    """Удаление карточки"""

    response = await client.delete(f"/cards/{created_card_id}")

    assert response.status_code == 204

    # Проверяем, что карточка действительно удалена
    get_response = await client.get(f"/cards/{created_card_id}")
    assert get_response.status_code == 404


@pytest.mark.anyio
async def test_get_cards_with_filters(client, created_card_id, sample_deck_id):
    """Получаем список карточек по deck_id"""

    response = await client.get(
        "/cards/",
        params={
            "deck_id": sample_deck_id,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
