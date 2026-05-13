from app.data.mock_data import MOCK_SCAN_SESSIONS
from app.schemas.common import MutationResponse
from app.schemas.scan import ScanSession


def create_scan_session() -> ScanSession:
    # TODO: Accept uploaded images and persist scan session metadata.
    return ScanSession(**MOCK_SCAN_SESSIONS["scan-1"])


def get_scan_session(scan_id: str) -> ScanSession | None:
    session = MOCK_SCAN_SESSIONS.get(scan_id)
    if not session:
        return None
    return ScanSession(**session)



def confirm_scan_candidate(scan_id: str, candidate_id: str) -> MutationResponse:
    # TODO: Decide whether confirmation immediately creates a collection entry
    # or first opens a pre-filled add-to-collection step for binder/condition details.
    return MutationResponse(
        success=True,
        message=f"Mock confirmation recorded for scan {scan_id} candidate {candidate_id}.",
    )
