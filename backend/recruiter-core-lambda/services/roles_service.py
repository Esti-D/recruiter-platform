import json
from datetime import datetime
import uuid

from models.store import ROLES, CANDIDATES, OFFERS


# ---------------------------
# Helpers
# ---------------------------

def _m(v):
    return v.lower() if isinstance(v, str) else v


# ---------------------------
# SERVICES
# ---------------------------

# GET /roles
def list_roles_service(event):
    params = event.get("queryStringParameters") or {}
    q = params.get("q")

    if not q:
        return 200, list(ROLES.values())

    data = [r for r in ROLES.values() if q.lower() in r["name"].lower()]
    return 200, data


# POST /roles
def create_role_service(event):
    body_raw = event.get("body") or "{}"
    body = json.loads(body_raw)

    rid = str(uuid.uuid4())

    role = {
        "roleId": rid,
        "name": body.get("name"),
        "createdAt": datetime.utcnow().isoformat()
    }

    ROLES[rid] = role
    return 201, role


# GET /roles/{role_id}
def get_role_service(event, role_id: str):
    r = ROLES.get(role_id)
    if not r:
        return 404, {"error": "not_found"}
    return 200, r


# PATCH /roles/{role_id}
def update_role_service(event, role_id: str):
    r = ROLES.get(role_id)
    if not r:
        return 404, {"error": "not_found"}

    body_raw = event.get("body") or "{}"
    body = json.loads(body_raw)

    for k, v in body.items():
        r[k] = v

    return 200, r


# DELETE /roles/{role_id}
def delete_role_service(event, role_id: str):
    # check role header
    headers = event.get("headers") or {}
    headers_lower = {k.lower(): v for k, v in headers.items()}
    role = headers_lower.get("x-role", "recruiter")

    if role != "admin":
        return 403, {"error": "forbidden"}

    if role_id not in ROLES:
        return 404, {"error": "not_found"}

    # comprobar si el rol está en uso
    usado_en_candidatos = any(c.get("role") == role_id for c in CANDIDATES.values())
    usado_en_ofertas = any(o.get("role") == role_id for o in OFFERS.values())

    if usado_en_candidatos or usado_en_ofertas:
        return 409, {"error": "role_in_use"}

    ROLES.pop(role_id)
    return 200, {"deleted": role_id}


# POST /roles/{role_id}/reassign
def reassign_role_service(event, role_id: str):
    # check role header
    headers = event.get("headers") or {}
    headers_lower = {k.lower(): v for k, v in headers.items()}
    role = headers_lower.get("x-role", "recruiter")

    if role != "admin":
        return 403, {"error": "forbidden"}

    if role_id not in ROLES:
        return 404, {"error": "not_found"}

    body_raw = event.get("body") or "{}"
    payload = json.loads(body_raw)
    new_role = payload.get("newRoleId")

    if not new_role or new_role not in ROLES:
        return 400, {"error": "invalid_new_role"}

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

    return 200, {"old": role_id, "new": new_role, "status": "updated_and_deleted"}
