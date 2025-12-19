from uuid import uuid4, UUID
from fastapi import APIRouter, HTTPException, status, Body, Path
from typing import List

from src.infrastructure.db.in_memory import _fake_cards_db, _fake_decks_db

from src.presentation.api.rest.v1.schemas.deck import (
    DeckCreate,
    DeckResponse,
    DeckUpdate,
)

router = APIRouter(
    prefix="/decks",
    tags=["Decks"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/",
    response_model=DeckResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новую колоду",
    description="Создаёт колоду добавляет в БД и сразу присваивает ID",
    responses={
        201: {"description": "Колода успешно создана"},
        422: {"description": "Ошибка валидации данных"},
    },
)
async def create_deck(deck_data: DeckCreate) -> DeckResponse:
    """
    Создание новой колоды.

    - **name**: название колоды
    - **description**: описание колоды
    """

    # Генерируем ID
    deck_id = uuid4()
    # today = date.today()

    deck_response = DeckResponse(
        id=deck_id, name=deck_data.name, description=deck_data.description
    )

    # Сохраняем в "базу"
    _fake_decks_db[str(deck_id)] = dict(deck_response)

    # Возвращаем через Pydantic модель (автоматическая сериализация)
    return deck_response


@router.get(
    "/{deck_id}",
    status_code=status.HTTP_200_OK,
    summary="Получить колод по deck_id",
    description="Возвращает полные данные одной колоды по её ID.",
    responses={200: {"description": "Колода успешно возвращена"}},
)
async def get_deck(
    deck_id: UUID = Path(
        ...,
        description="Уникальный идентификатор колоды",
        examples=["a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8"],
    ),
) -> DeckResponse:
    deck_record = _fake_decks_db.get(str(deck_id))
    if not deck_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Колода с ID {deck_id} не существует",
        )

    return DeckResponse(**deck_record)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Получить список всех колод",
    description="Возвращает список всех колод.",
    responses={200: {"description": "Колоды успешно возвращены"}},
)
async def get_decks() -> List[DeckResponse]:
    decks_record = _fake_decks_db.values()
    if not decks_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Колод не существует"
        )

    return [DeckResponse(**deck) for deck in decks_record]


@router.patch(
    "/{deck_id}",
    status_code=status.HTTP_200_OK,
    summary="Частично изменяет колоду по deck_id",
    description="Обновляет только переданные поля колоды name и/или description",
    responses={
        200: {"description": "Колода успешно изменена"},
        404: {"description": "Колода с указанным ID не существует"},
        422: {
            "description": "Ошибка валидации (например, передана пустая строка на изменение"
        },
    },
)
async def update_deck(
    deck_id: UUID = Path(
        ..., description="ID колоды", examples=["a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8"]
    ),
    update_data: DeckUpdate = Body(
        ..., description="Поля для обновения. Можно передать как одно так и все."
    ),
) -> DeckResponse:
    """
    Частичное обновление колоды.

    - Если поле не передано или пустое — остаётся без изменений
    """

    deck_record = _fake_decks_db.get(str(deck_id))

    if not deck_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Колода с ID {deck_id} не существует",
        )

    # Обновляем только те поля, которые пришли и не None
    if update_data.name:
        deck_record["name"] = update_data.name.strip()

    if update_data.description:
        deck_record["description"] = update_data.description.strip()

    # Сохраняем изменения
    _fake_decks_db[str(deck_id)] = deck_record

    # Возвращаем обновлённую карточку
    return DeckResponse(**deck_record)


@router.delete(
    "/{deck_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удаляет колоду по deck_id",
    description="Безвозвратно удаляет колоду и все связанные с ней карточки по ее ID",
    responses={
        204: {"description": "Колода успешно удалена"},
        404: {"description": "Колода с указанным ID не существует"},
    },
)
async def delete_card(
    deck_id: UUID = Path(
        ..., description="ID колоды", examples=["a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8"]
    ),
) -> None:
    """
    Удаление колоды.

    - Если колоды существует — удаляется из "базы"
    - Если нет — 404
    - Успешное удаление — 204 No Content (тела ответа нет)
    """
    # проверяем на наличие карточки в БД
    deck_key = str(deck_id)
    if deck_key not in _fake_cards_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"карточка с ID - {deck_id} не найдена",
        )

    # Удаляем из БД
    del _fake_decks_db[deck_key]

    return None
