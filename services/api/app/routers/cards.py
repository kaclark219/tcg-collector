from urllib.request import Request, urlopen

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import Response

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


@router.get("/{card_id}/image")
def get_card_image_route(card_id: str) -> Response:
    card = get_card(card_id)
    if card is None:
        raise HTTPException(status_code=404, detail="Card not found")

    if not card.image_url:
        raise HTTPException(status_code=404, detail="Card image not found")

    try:
        request = Request(
            card.image_url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (compatible; tcg-collector/1.0; +http://localhost)"
                )
            },
        )
        with urlopen(request, timeout=20) as upstream:
            body = upstream.read()
            content_type = upstream.headers.get("Content-Type", "image/png")
            return Response(content=body, media_type=content_type)
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Unable to fetch upstream card image: {exc}",
        ) from exc
