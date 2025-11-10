from fastapi import APIRouter, HTTPException
from src.shared.models import ProcessIn, ProcessOut
from src.offers.store import OFFERS
from .store import PROCESSES
import uuid

router = APIRouter()

@router.post("", response_model=ProcessOut)
def create_process(body: ProcessIn):
    if body.offerId not in OFFERS:
        raise HTTPException(404, "offer not found")
    process_id = str(uuid.uuid4())
    PROCESSES[process_id] = {"offerId": body.offerId, "status": "READY"}
    return ProcessOut(processId=process_id, offerId=body.offerId)
