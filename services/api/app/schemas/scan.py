from pydantic import BaseModel


class ScanCandidate(BaseModel):
    id: str
    card_id: str
    confidence: float
    reason: str


class ScanSession(BaseModel):
    id: str
    status: str
    image_url: str | None = None
    candidates: list[ScanCandidate]


class CreateScanRequest(BaseModel):
    mode: str = "mock"


class ConfirmScanCandidateRequest(BaseModel):
    candidate_id: str

