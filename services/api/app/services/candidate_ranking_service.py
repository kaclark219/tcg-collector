from app.schemas.scan import ScanCandidate


def rank_candidates(candidates: list[ScanCandidate]) -> list[ScanCandidate]:
    # TODO: Combine OCR confidence, visual similarity, and set/number heuristics.
    return sorted(candidates, key=lambda candidate: candidate.confidence, reverse=True)

