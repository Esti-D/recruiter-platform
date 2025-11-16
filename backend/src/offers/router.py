from fastapi import APIRouter, HTTPException, Header, Query
from datetime import datetime
import uuid
from src.shared.models import OfferIn, OfferOut, OfferUpdate
from .store import OFFERS

router = APIRouter()

# Crear oferta
@router.post("", response_model=OfferOut)
def create_offer(body: OfferIn):
    offer_id = str(uuid.uuid4())
    OFFERS[offer_id] = data = body.model_dump() | {
        "offerId": offer_id,
        "createdAt": datetime.utcnow(),
    }
    return data


# Listar ofertas con filtros
@router.get("", response_model=list[OfferOut])
def list_offers(
    q: str | None = None,
    companyName: str | None = None,
    contactPerson: str | None = None,
    role: str | None = None,
    modality: str | None = None,
    location: str | None = None,
):
    def matches(o):
        def m(x): return x.lower() if isinstance(x, str) else x
        if q and not any(m(q) in m(str(o.get(k, ""))) for k in ("companyName", "role", "description")):
            return False
        if companyName and m(companyName) != m(o.get("companyName")):
            return False
        if contactPerson and m(contactPerson) != m(o.get("contactPerson")):
            return False
        if role and m(role) != m(o.get("role")):
            return False
        if modality and m(modality) != m(o.get("modality")):
            return False
        if location and m(location) != m(o.get("location")):
            return False
        return True

    return [v for v in OFFERS.values() if matches(v)]


# Obtener detalle
@router.get("/{offer_id}", response_model=OfferOut)
def get_offer(offer_id: str):
    offer = OFFERS.get(offer_id)
    if not offer:
        raise HTTPException(404, detail="not found")
    return offer


# Editar oferta
@router.patch("/{offer_id}", response_model=OfferOut)
def update_offer(offer_id: str, body: OfferUpdate):
    offer = OFFERS.get(offer_id)
    if not offer:
        raise HTTPException(404, detail="not found")
    for k, v in body.model_dump(exclude_unset=True).items():
        offer[k] = v
    offer["updatedAt"] = datetime.utcnow()
    return offer


# Eliminar oferta
@router.delete("/{offer_id}")
def delete_offer(offer_id: str, x_role: str = Header(default="recruiter")):
    if x_role != "admin":
        raise HTTPException(403, detail="forbidden")
    if offer_id not in OFFERS:
        raise HTTPException(404, detail="not found")
    OFFERS.pop(offer_id)
    return {"deleted": offer_id}
