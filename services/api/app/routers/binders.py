from fastapi import APIRouter, HTTPException, Query

from app.schemas.binders import Binder
from app.schemas.binders_requests import CreateBinderRequest
from app.services.binder_service import BinderCreationError, create_binder, get_binder, list_binders

router = APIRouter(prefix="/binders", tags=["binders"])


@router.get("", response_model=list[Binder])
def list_binders_route(profile_id: str | None = Query(default=None)) -> list[Binder]:
    return list_binders(profile_id)


@router.get("/{binder_id}", response_model=Binder)
def get_binder_route(
    binder_id: str,
    profile_id: str | None = Query(default=None),
) -> Binder:
    binder = get_binder(binder_id, profile_id)
    if binder is None:
        raise HTTPException(status_code=404, detail="Binder not found")
    return binder


@router.post("", response_model=Binder, status_code=201)
def create_binder_route(request: CreateBinderRequest) -> Binder:
    try:
        return create_binder(request.profile_id, request.name, request.description)
    except BinderCreationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
