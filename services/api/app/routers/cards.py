from fastapi import APIRouter, HTTPException, Query

from app.schemas.cards import Card, CardSearchResponse
from app.services.card_search_service import get_card, search_cards

router = APIRouter(prefix="/cards", tags=["cards"])


@router.get("/search", response_model=CardSearchResponse)
def search_cards_route(q: str = Query(default="")) -> CardSearchResponse:
    return CardSearchResponse(cards=search_cards(q))


@router.get("/{card_id}", response_model=Card)
def get_card_route(card_id: str) -> Card:
    card = get_card(card_id)
    if card is None:
        raise HTTPException(status_code=404, detail="Card not found")
    return card

