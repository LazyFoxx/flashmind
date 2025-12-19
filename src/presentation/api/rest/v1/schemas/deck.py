from uuid import UUID
from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


class DeckCreate(BaseModel):
    """Схема для создания новой колоды"""

    name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Название колоды",
        examples=["REST API"],
    )
    description: str = Field(
        ...,
        min_length=0,
        max_length=2000,
        description="Описание колоды",
        examples=[
            "Колода REST API содержит карточки для изучения и улучшения знаний технологии"
        ],
    )


class DeckResponse(BaseModel):
    """Схема ответа — как выглядит колода после создания"""

    id: UUID
    name: str
    description: str

    model_config = {
        "from_attributes": True,  # позволяет создавать из ORM/датаклассов
        "json_encoders": {date: lambda v: v.isoformat()},
    }


class DeckUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

    model_config = {"extra": "forbid"}
