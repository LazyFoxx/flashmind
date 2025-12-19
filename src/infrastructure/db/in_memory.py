from typing import Dict

# Это наше in-memory хранилище
_fake_decks_db: Dict[str, dict] = {
    "550e8400-e29b-41d4-a716-446655440000": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "name": "Python",
        "description": "Язык пайтон самый лучший язык на планете",
    },
}


_fake_cards_db: dict[str, dict] = {}


__all__ = ["_fake_decks_db", "_fake_cards_db"]
