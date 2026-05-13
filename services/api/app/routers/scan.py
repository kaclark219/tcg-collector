from fastapi import APIRouter, HTTPException

from app.schemas.common import MutationResponse
from app.schemas.scan import ConfirmScanCandidateRequest, CreateScanRequest, ScanSession
from app.services.scan_pipeline import (
    confirm_scan_candidate,
    create_scan_session,
    get_scan_session,
)

router = APIRouter(prefix="/scan", tags=["scan"])


@router.post("", response_model=ScanSession)
def create_scan_route(_: CreateScanRequest) -> ScanSession:
    return create_scan_session()


@router.get("/{scan_id}", response_model=ScanSession)
def get_scan_route(scan_id: str) -> ScanSession:
    session = get_scan_session(scan_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Scan session not found")
    return session


@router.post("/{scan_id}/confirm", response_model=MutationResponse)
def confirm_scan_candidate_route(
    scan_id: str,
    request: ConfirmScanCandidateRequest,
) -> MutationResponse:
    return confirm_scan_candidate(scan_id, request.candidate_id)
