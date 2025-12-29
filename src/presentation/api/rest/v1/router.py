from fastapi import APIRouter
from src.presentation.api.rest.v1.endpoints.cards import router as v1_router_cards
from src.presentation.api.rest.v1.endpoints.decks import router as v1_router_decks


router = APIRouter()

# v1
router.include_router(
    v1_router_cards,
    prefix="/cards",
    tags=["Cards"],
    responses={404: {"description": "Not found"}},
)


router.include_router(
    v1_router_decks,
    prefix="/decks",
    tags=["Decks"],
    responses={404: {"description": "Not found"}},
)
