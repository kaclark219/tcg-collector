from uuid import UUID

from pydantic import BaseModel, Field


class Profile(BaseModel):
    id: UUID
    username: str


class CreateProfileRequest(BaseModel):
    username: str
    pin: str = Field(min_length=6, max_length=6)


class LoginRequest(BaseModel):
    username: str
    pin: str = Field(min_length=6, max_length=6)


class LoginResponse(BaseModel):
    profile: Profile

