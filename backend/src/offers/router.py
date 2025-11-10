from fastapi import APIRouter, HTTPException
from src.shared.models import OfferIn, OfferOut
from .store import OFFERS
router=APIRouter()
@router.post("", response_model=OfferOut)
def create_offer(body: OfferIn):
    if body.offerId in OFFERS: raise HTTPException(409,"offer exists")
    OFFERS[body.offerId]=body.model_dump(); return OfferOut(offerId=body.offerId)
