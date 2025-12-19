from uuid import UUID
from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


class CardCreate(BaseModel):
    """Схема для создания новой карточки"""

    deck_id: UUID = Field(
        ...,
        description="ID колоды, в которую добавляется карточка",
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    )
    front: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="Текст на лицевой стороне (вопрос)",
        examples=["Что такое REST API?"],
    )
    back: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Текст на обратной стороне (ответ)",
        examples=[
            "Representational State Transfer — архитектурный стиль для веб-сервисов"
        ],
    )


class CardResponse(BaseModel):
    """Схема ответа — как выглядит карточка после создания"""

    id: UUID
    deck_id: UUID
    front: str
    back: str
    ease_factor: float = Field(
        default=2.5, ge=1.3, description="Коэффициент лёгкости (SM-2 алгоритм)"
    )
    interval: int = Field(default=0, ge=0, description="Текущий интервал в днях")
    repetitions: int = Field(
        default=0, ge=0, description="Количество успешных повторений подряд"
    )
    due_date: date = Field(..., description="Дата следующего повторения")
    lapses: int = Field(default=0, ge=0, description="Количество провалов")

    model_config = {
        "from_attributes": True,  # позволяет создавать из ORM/датаклассов
        "json_encoders": {date: lambda v: v.isoformat()},
    }


class CardUpdate(BaseModel):
    front: Optional[str] = None
    back: Optional[str] = None

    model_config = {"extra": "forbid"}
