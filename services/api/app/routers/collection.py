from fastapi import APIRouter, HTTPException, Query

from app.schemas.collection import (
    CollectionEntry,
    CreateCollectionEntryRequest,
    MoveCollectionEntryRequest,
)
from app.schemas.common import MutationResponse
from app.services.collection_service import (
    CollectionCreationError,
    CollectionDeletionError,
    CollectionMoveError,
    create_collection_entry,
    delete_collection_entry,
    get_collection_entry,
    list_collection_entries,
    move_collection_entry,
)

router = APIRouter(prefix="/collection", tags=["collection"])


@router.get("", response_model=list[CollectionEntry])
def list_collection_route(
    profile_id: str = Query(...),
    binder_id: str | None = Query(default=None),
) -> list[CollectionEntry]:
    return list_collection_entries(profile_id, binder_id)


@router.get("/{entry_id}", response_model=CollectionEntry)
def get_collection_entry_route(entry_id: str) -> CollectionEntry:
    entry = get_collection_entry(entry_id)
    if entry is None:
        raise HTTPException(status_code=404, detail="Collection entry not found")
    return entry


@router.post("", response_model=CollectionEntry, status_code=201)
def create_collection_entry_route(
    request: CreateCollectionEntryRequest,
) -> CollectionEntry:
    try:
        return create_collection_entry(
            profile_id=request.profile_id,
            card_id=request.card_id,
            binder_id=request.binder_id,
            variant=request.variant,
            notes=request.notes,
        )
    except CollectionCreationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/move", response_model=MutationResponse)
def move_collection_entry_route(
    request: MoveCollectionEntryRequest,
) -> MutationResponse:
    try:
        return move_collection_entry(request.entry_id, request.binder_id)
    except CollectionMoveError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.delete("/{entry_id}", response_model=MutationResponse)
def delete_collection_entry_route(entry_id: str) -> MutationResponse:
    try:
        return delete_collection_entry(entry_id)
    except CollectionDeletionError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
