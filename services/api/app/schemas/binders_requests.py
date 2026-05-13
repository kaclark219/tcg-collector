from pydantic import BaseModel


class CreateBinderRequest(BaseModel):
    profile_id: str
    name: str
    description: str | None = None

