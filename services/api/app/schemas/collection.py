from pydantic import BaseModel


class CollectionEntry(BaseModel):
    id: str
    profile_id: str
    card_id: str
    binder_id: str
    variant: str
    notes: str | None = None


class CreateCollectionEntryRequest(BaseModel):
    profile_id: str
    card_id: str
    binder_id: str
    variant: str = "unknown"
    notes: str | None = None


class MoveCollectionEntryRequest(BaseModel):
    entry_id: str
    binder_id: str

