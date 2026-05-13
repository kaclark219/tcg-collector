from pydantic import BaseModel


class Binder(BaseModel):
    id: str
    name: str
    description: str | None = None
    entry_count: int
