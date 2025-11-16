from fastapi import APIRouter, HTTPException, Header
from datetime import datetime
import uuid
from src.shared.models import CandidateIn, CandidateOut, CandidateUpdate
from .store import CANDIDATES

router = APIRouter()

@router.post("", response_model=CandidateOut)
def create_candidate(body: CandidateIn):
    cid = str(uuid.uuid4())
    CANDIDATES[cid] = d = body.model_dump() | {"candidateId": cid, "createdAt": datetime.utcnow()}
    return d

@router.get("", response_model=list[CandidateOut])
def list_candidates(q: str | None = None, role: str | None = None,
                    location: str | None = None, status: str | None = None):
    def m(v): return v.lower() if isinstance(v, str) else v
    def ok(c):
        if q and not any(m(q) in m(str(c.get(k,""))) for k in ("name","dni","role","location","notes")): return False
        if role and m(role) != m(c.get("role")): return False
        if location and m(location) != m(c.get("location")): return False
        if status and m(status) != m(c.get("status")): return False
        return True
    return [v for v in CANDIDATES.values() if ok(v)]

@router.get("/{candidate_id}", response_model=CandidateOut)
def get_candidate(candidate_id: str):
    c = CANDIDATES.get(candidate_id)
    if not c: raise HTTPException(404, "not found")
    return c

@router.patch("/{candidate_id}", response_model=CandidateOut)
def update_candidate(candidate_id: str, body: CandidateUpdate):
    c = CANDIDATES.get(candidate_id)
    if not c: raise HTTPException(404, "not found")
    for k,v in body.model_dump(exclude_unset=True).items(): c[k]=v
    c["updatedAt"] = datetime.utcnow(); return c

@router.delete("/{candidate_id}")
def delete_candidate(candidate_id: str, x_role: str = Header(default="recruiter")):
    if x_role != "admin": raise HTTPException(403, "forbidden")
    if candidate_id not in CANDIDATES: raise HTTPException(404, "not found")
    CANDIDATES.pop(candidate_id); return {"deleted": candidate_id}
