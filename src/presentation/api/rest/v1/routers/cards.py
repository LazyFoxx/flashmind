from uuid import uuid4, UUID
from datetime import date
from fastapi import APIRouter, HTTPException, status, Query, Body, Path
from typing import List

from src.infrastructure.db.in_memory import _fake_cards_db, _fake_decks_db

from src.presentation.api.rest.v1.schemas.card import (
    CardCreate,
    CardResponse,
    CardUpdate,
)

router = APIRouter(
    prefix="/cards",
    tags=["Cards"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/",
    response_model=CardResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новую карточку",
    description="Создаёт карточку в указанной колоде. Новые карточки сразу доступны для изучения (due_date = сегодня)",
    responses={
        201: {"description": "Карточка успешно создана"},
        404: {"description": "Колоды не существует"},
        422: {"description": "Ошибка валидации данных"},
    },
)
async def create_card(card_data: CardCreate) -> CardResponse:
    """
    Создание новой карточки.

    - **deck_id**: обязателен, проверяется на существование
    - **front**: вопрос/лицевая сторона
    - **back**: ответ/обратная сторона
    """

    if str(card_data.deck_id) not in _fake_decks_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Колоды с ID {card_data.deck_id} не существует",
        )
        return card_data.deck_id

    # Генерируем ID и начальные значения по алгоритму Spaced Repetition (SM-2)
    card_id = uuid4()
    today = date.today()

    card_record: CardResponse = CardResponse(
        id=card_id,
        deck_id=card_data.deck_id,
        front=card_data.front.strip(),
        back=card_data.back.strip(),
        ease_factor=2.5,
        interval=0,  # новая карточка → первый повтор сегодня
        repetitions=0,
        due_date=today,
        lapses=0,
    )

    # Сохраняем в "базу"
    _fake_cards_db[str(card_id)] = dict(card_record)

    # Возвращаем через Pydantic модель (автоматическая сериализация)
    return card_record


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Получить список карточек",
    description="Возвращает все карточки пользователя. "
    "Опционально можно фильтровать по колоде через параметр `deck_id`.",
    responses={200: {"description": "Список карточек успешно возвращен"}},
)
async def get_cards(
    deck_id: UUID | None = Query(
        None,
        description="Фильтр: вернуть только карточки из указанной по ID колоды",
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    ),
) -> List[CardResponse]:
    """
    Получение списка карточек.

    - Без параметров — все карточки
    - С ?deck_id=... — только из конкретной колоды
    """
    # Берём все карточки из "базы"
    cards = _fake_cards_db.values()

    # Если передан deck_id — фильтруем
    if deck_id is not None:
        filtered_cards = [card for card in cards if UUID(card["deck_id"]) == deck_id]
    else:
        filtered_cards = list(cards)

    # Преобразуем в Pydantic-модели для корректной сериализации
    return [CardResponse(**card) for card in filtered_cards]


@router.get(
    "/{card_id}",
    status_code=status.HTTP_200_OK,
    summary="Получить карточку по card_id",
    description="Возвращает полные данные одной карточки по её уникальному идентификатору.",
    responses={200: {"description": "Карточка успешно возвращена"}},
)
async def get_card(
    card_id: UUID = Path(
        ...,
        description="Уникальный идентификатор карточки",
        examples=["a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8"],
    ),
) -> CardResponse:
    card_record = _fake_cards_db.get(str(card_id))
    if not card_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Карточка с ID {card_id} не существует",
        )

    return CardResponse(**card_record)


@router.patch(
    "/{card_id}",
    status_code=status.HTTP_200_OK,
    summary="Частично изменяет карточку по card_id",
    description="Обновляет только переданные поля карточки front и/или back",
    responses={
        200: {"description": "Карточка успешно изменена"},
        404: {"description": "Карточка с указанным ID не существует"},
        422: {"description": "Ошибка валидации (например, пустая строка в front/back)"},
    },
)
async def update_card(
    card_id: UUID = Path(
        ...,
        description="Уникальный идентификатор карточки",
        examples=["a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8"],
    ),
    update_data: CardUpdate = Body(
        ..., description="Поля для обновения. Можно передать как одно так и оба."
    ),
) -> CardResponse:
    """
    Частичное обновление карточки.

    - Если поле не передано или пустое — остаётся без изменений
    """

    card_record = _fake_cards_db.get(str(card_id))

    if not card_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Карточка с ID {card_id} не существует",
        )

    # Обновляем только те поля, которые пришли и не None
    if update_data.front:
        card_record["front"] = update_data.front.strip()

    if update_data.back:
        card_record["back"] = update_data.back.strip()

    # Сохраняем изменения
    _fake_cards_db[str(card_id)] = card_record

    # Возвращаем обновлённую карточку
    return CardResponse(**card_record)


@router.delete(
    "/{card_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удаляет карточку по card_id",
    description="Безвозвратно удаляет карточку по ее ID",
    responses={
        204: {"description": "Карточка успешно удалена"},
        404: {"description": "Карточка с указанным ID не существует"},
    },
)
async def delete_card(
    card_id: UUID = Path(
        ...,
        description="Уникальный идентификатор карточки",
        examples=["a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8"],
    ),
) -> None:
    """
    Удаление карточки.

    - Если карточка существует — удаляется из "базы"
    - Если нет — 404
    - Успешное удаление — 204 No Content (тела ответа нет)
    """
    # проверяем на наличие карточки в БД
    card_key = str(card_id)
    if card_key not in _fake_cards_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"карточка с ID - {card_id} не найдена",
        )

    # Удаляем из БД
    del _fake_cards_db[card_key]

    return None
