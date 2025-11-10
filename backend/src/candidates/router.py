from fastapi import APIRouter, Query
from src.shared.models import CandidateOut
from .store import CANDIDATES

router = APIRouter()

@router.get("", response_model=list[CandidateOut])
def get_candidates(role: str | None = None, skills: str | None = None):
    data = CANDIDATES
    if role:
        data = [c for c in data if c["role"].lower() == role.lower()]
    if skills:
        wanted = {s.strip().lower() for s in skills.split(",")}
        data = [c for c in data if wanted.intersection(set(map(str.lower, c["skills"])))]
    return data
