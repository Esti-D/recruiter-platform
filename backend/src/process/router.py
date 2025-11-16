from fastapi import APIRouter, HTTPException
from datetime import datetime; import uuid
from src.shared.models import ProcessIn, ProcessOut, ProcessUpdate, CandidateInProcess
from .store import PROCESSES
from src.offers.store import OFFERS
from src.candidates.store import CANDIDATES

router = APIRouter()

@router.post("", response_model=ProcessOut)
def create_process(body: ProcessIn):
    off = next((v for v in OFFERS.values() if v["offerId"]==body.offerId), None)
    if not off: raise HTTPException(404, "offer not found")
    pid=str(uuid.uuid4())
    p={"processId":pid,"offerId":body.offerId,"roleOffer":off["role"],"similarRoles":[],"recruiter":body.recruiter,
       "notes":body.notes,"status":"OPEN","createdAt":datetime.utcnow(),"closedAt":None,"candidates":[]}
    PROCESSES[pid]=p; return p

@router.get("", response_model=list[ProcessOut])
def list_processes(offerId:str|None=None,status:str|None=None):
    def ok(x): return (not offerId or x["offerId"]==offerId) and (not status or x["status"]==status)
    return [v for v in PROCESSES.values() if ok(v)]

@router.get("/{pid}", response_model=ProcessOut)
def get_process(pid:str):
    p=PROCESSES.get(pid); 
    if not p: 
        raise HTTPException(404,"not found"); 
    return p

@router.patch("/{pid}", response_model=ProcessOut)
def update_process(pid:str, body:ProcessUpdate):
    p=PROCESSES.get(pid); 
    if not p: raise HTTPException(404,"not found")
    for k,v in body.model_dump(exclude_unset=True).items(): p[k]=v
    if p.get("status")=="CLOSED" and not p.get("closedAt"): p["closedAt"]=datetime.utcnow()
    return p

@router.post("/{pid}/candidates:generate")
def generate_candidates(pid:str, payload:dict):
    p=PROCESSES.get(pid); 
    if not p: raise HTTPException(404,"not found")
    roles={p["roleOffer"], *payload.get("similarRoles",[])}
    selected=[c for c in CANDIDATES.values() if c.get("status","OPEN")=="OPEN" and c.get("role") in roles]
    p["similarRoles"]=payload.get("similarRoles",[])
    p["candidates"]=[CandidateInProcess(
        candidateId=c["candidateId"], name=c["name"], role=c["role"],
        experience=c.get("experience"), strength=c.get("strength"),
        salaryRange=c.get("salaryRange")
    ).model_dump() for c in selected]
    return {"processId": pid, "count": len(p["candidates"])}
