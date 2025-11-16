from fastapi import APIRouter, HTTPException, Header
from datetime import datetime
import uuid

from src.shared.models import RoleIn, RoleOut, RoleUpdate
from .store import ROLES

router = APIRouter()

@router.post("", response_model=RoleOut)
def create_role(body: RoleIn):
    rid = str(uuid.uuid4())
    ROLES[rid] = data = {
        "roleId": rid,
        "name": body.name,
        "createdAt": datetime.utcnow()
    }
    return data

@router.get("", response_model=list[RoleOut])
def list_roles(q: str | None = None):
    if not q:
        return list(ROLES.values())
    return [r for r in ROLES.values() if q.lower() in r["name"].lower()]

@router.get("/{role_id}", response_model=RoleOut)
def get_role(role_id: str):
    r = ROLES.get(role_id)
    if not r:
        raise HTTPException(404, "not found")
    return r

@router.patch("/{role_id}", response_model=RoleOut)
def update_role(role_id: str, body: RoleUpdate):
    r = ROLES.get(role_id)
    if not r:
        raise HTTPException(404, "not found")
    for k, v in body.model_dump(exclude_unset=True).items():
        r[k] = v
    return r

@router.delete("/{role_id}")
def delete_role(role_id: str, x_role: str = Header(default="recruiter")):
    from src.candidates.store import CANDIDATES
    from src.offers.store import OFFERS

    if x_role != "admin":
        raise HTTPException(403, "forbidden")
    if role_id not in ROLES:
        raise HTTPException(404, "not found")

    # --- 🔒 COMPROBAR SI EL ROL ESTÁ EN USO ---
    usado_en_candidatos = any(c.get("role") == role_id for c in CANDIDATES.values())
    usado_en_ofertas = any(o.get("role") == role_id for o in OFFERS.values())

    if usado_en_candidatos or usado_en_ofertas:
        raise HTTPException(409, detail="role_in_use")

    # --- SI NO ESTÁ EN USO, BORRAR ---
    ROLES.pop(role_id)
    return {"deleted": role_id}

@router.post("/{role_id}/reassign")
def reassign_role(role_id: str, payload: dict, x_role: str = Header(default="recruiter")):
    """
    Reasigna el role_id a otro roleId antes de eliminarlo.
    payload = { "newRoleId": "xxx" }
    """
    if x_role != "admin":
        raise HTTPException(403, "forbidden")

    from src.candidates.store import CANDIDATES
    from src.offers.store import OFFERS

    if role_id not in ROLES:
        raise HTTPException(404, "not found")

    new_role = payload.get("newRoleId")
    if not new_role or new_role not in ROLES:
        raise HTTPException(400, "invalid_new_role")

    # 1. Reasignar candidatos
    for c in CANDIDATES.values():
        if c.get("role") == role_id:
            c["role"] = new_role

    # 2. Reasignar ofertas
    for o in OFFERS.values():
        if o.get("role") == role_id:
            o["role"] = new_role

    # 3. Eliminar rol viejo
    ROLES.pop(role_id)

    return {"old": role_id, "new": new_role, "status": "updated_and_deleted"}
