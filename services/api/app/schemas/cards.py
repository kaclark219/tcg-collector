from pydantic import BaseModel


class Card(BaseModel):
    id: str
    name: str
    set_name: str
    number: str
    rarity: str
    image_url: str | None = None
    category: str | None = None
    illustrator: str | None = None
    set_id: str | None = None
    variant_normal: bool = False
    variant_reverse: bool = False
    variant_holo: bool = False
    variant_first_edition: bool = False
    variant_w_promo: bool = False


class CardSearchResponse(BaseModel):
    cards: list[Card]
