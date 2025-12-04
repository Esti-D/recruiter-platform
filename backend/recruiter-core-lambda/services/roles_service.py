import json
from datetime import datetime
import uuid

from models.store import roles_table, candidates_table, offers_table


def _m(v):
    return v.lower() if isinstance(v, str) else v


def _scan_all(table):
    """Lee todos los items de una tabla Dynamo con paginación."""
    items: list[dict] = []
    resp = table.scan()
    items.extend(resp.get("Items", []))

    while "LastEvaluatedKey" in resp:
        resp = table.scan(ExclusiveStartKey=resp["LastEvaluatedKey"])
        items.extend(resp.get("Items", []))

    return items


# ==========================================
# GET /roles
# ==========================================
def list_roles_service(event):
    params = event.get("queryStringParameters") or {}
    q = params.get("q")

    items = _scan_all(roles_table)

    if not q:
        return 200, items

    q_lower = q.lower()
    data = [r for r in items if q_lower in r.get("name", "").lower()]
    return 200, data


# ==========================================
# POST /roles
# ==========================================
def create_role_service(event):
    body_raw = event.get("body") or "{}"
    body = json.loads(body_raw)

    rid = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()

    role = {
        "roleId": rid,
        "name": body.get("name", ""),
        "createdAt": now,
    }

    roles_table.put_item(Item=role)
    return 201, role


# ==========================================
# GET /roles/{role_id}
# ==========================================
def get_role_service(event, role_id: str):
    resp = roles_table.get_item(Key={"roleId": role_id})
    r = resp.get("Item")
    if not r:
        return 404, {"error": "not_found"}
    return 200, r


# ==========================================
# PATCH /roles/{role_id}
# ==========================================
def update_role_service(event, role_id: str):
    resp = roles_table.get_item(Key={"roleId": role_id})
    r = resp.get("Item")
    if not r:
        return 404, {"error": "not_found"}

    body_raw = event.get("body") or "{}"
    body = json.loads(body_raw)

    for k, v in body.items():
        r[k] = v

    r["updatedAt"] = datetime.utcnow().isoformat()
    roles_table.put_item(Item=r)

    return 200, r


# ==========================================
# DELETE /roles/{role_id}
# ==========================================
def delete_role_service(event, role_id: str):
    headers = event.get("headers") or {}
    headers_lower = {k.lower(): v for k, v in headers.items()}
    role_header = headers_lower.get("x-role", "recruiter")

    if role_header not in ("admin", "recruiter"):
        return 403, {"error": "forbidden"}

    # comprobar si existe el rol
    resp = roles_table.get_item(Key={"roleId": role_id})
    if "Item" not in resp:
        return 404, {"error": "not_found"}

    # comprobar si el rol está en uso en candidatos u ofertas
    candidatos = _scan_all(candidates_table)
    ofertas = _scan_all(offers_table)

    usado_en_candidatos = any(_m(c.get("role")) == _m(role_id) for c in candidatos)
    usado_en_ofertas = any(_m(o.get("role")) == _m(role_id) for o in ofertas)

    if usado_en_candidatos or usado_en_ofertas:
        return 409, {"error": "role_in_use"}

    roles_table.delete_item(Key={"roleId": role_id})
    return 200, {"deleted": role_id}


# ==========================================
# POST /roles/{role_id}/reassign
# ==========================================
def reassign_role_service(event, role_id: str):
    headers = event.get("headers") or {}
    headers_lower = {k.lower(): v for k, v in headers.items()}
    role_header = headers_lower.get("x-role", "recruiter")

    # Igual que en delete_role_service: permitimos admin y recruiter
    if role_header not in ("admin", "recruiter"):
        return 403, {"error": "forbidden"}

    # comprobar rol origen
    resp = roles_table.get_item(Key={"roleId": role_id})
    if "Item" not in resp:
        return 404, {"error": "not_found"}

    body_raw = event.get("body") or "{}"
    payload = json.loads(body_raw)
    new_role = payload.get("newRoleId")

    if not new_role:
        return 400, {"error": "invalid_new_role"}

    # comprobar que el rol destino existe
    resp_new = roles_table.get_item(Key={"roleId": new_role})
    if "Item" not in resp_new:
        return 400, {"error": "invalid_new_role"}

    # 1. Reasignar candidatos
    candidatos = _scan_all(candidates_table)
    for c in candidatos:
        if _m(c.get("role")) == _m(role_id):
            c["role"] = new_role
            candidates_table.put_item(Item=c)

    # 2. Reasignar ofertas
    ofertas = _scan_all(offers_table)
    for o in ofertas:
        if _m(o.get("role")) == _m(role_id):
            o["role"] = new_role
            offers_table.put_item(Item=o)

    # 3. Eliminar rol viejo
    roles_table.delete_item(Key={"roleId": role_id})

    return 200, {
        "old": role_id,
        "new": new_role,
        "status": "updated_and_deleted",
    }

