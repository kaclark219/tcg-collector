from fastapi import APIRouter, HTTPException

from app.schemas.profiles import CreateProfileRequest, LoginRequest, LoginResponse, Profile
from app.services.auth_service import (
    AuthenticationError,
    InvalidPinError,
    ProfileAlreadyExistsError,
    create_profile,
    login_profile,
)

router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.post("", response_model=Profile, status_code=201)
def create_profile_route(request: CreateProfileRequest) -> Profile:
    try:
        return create_profile(request.username, request.pin)
    except InvalidPinError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except ProfileAlreadyExistsError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.post("/login", response_model=LoginResponse)
def login_profile_route(request: LoginRequest) -> LoginResponse:
    try:
        profile = login_profile(request.username, request.pin)
    except InvalidPinError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except AuthenticationError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc

    return LoginResponse(profile=profile)

