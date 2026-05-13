from pydantic import BaseModel


class MutationResponse(BaseModel):
    success: bool
    message: str

