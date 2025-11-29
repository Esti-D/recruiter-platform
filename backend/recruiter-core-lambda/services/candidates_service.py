import json
from datetime import datetime
import uuid

from models.store import candidates_table  # antes: CANDIDATES dict


def _m(v):
    return v.lower() if isinstance(v, str) else v


def _scan_all(table):
    """Lee todos los items de la tabla (con paginación)."""
    items: list[dict] = []
    resp = table.scan()
    items.extend(resp.get("Items", []))

    while "LastEvaluatedKey" in resp:
        resp = table.scan(ExclusiveStartKey=resp["LastEvaluatedKey"])
        items.extend(resp.get("Items", []))

    return items


# GET /candidates
def list_candidates_service(event):
    params = event.get("queryStringParameters") or {}

    q = params.get("q")
    role = params.get("role")
    location = params.get("location")
    status = params.get("status")

    def ok(c: dict):
        if q and not any(
            _m(q) in _m(str(c.get(k, "")))
            for k in ("name", "dni", "role", "location", "notes")
        ):
            return False
        if role and _m(role) != _m(c.get("role")):
            return False
        if location and _m(location) != _m(c.get("location")):
            return False
        if status and _m(status) != _m(c.get("status")):
            return False
        return True

    items = _scan_all(candidates_table)
    data = [v for v in items if ok(v)]
    return 200, data


# POST /candidates
def create_candidate_service(event):
    body_raw = event.get("body") or "{}"
    body = json.loads(body_raw)

    cid = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()

    status = body.get("status") or "OPEN_TO_LISTEN"
    if status not in ("OPEN_TO_LISTEN", "NOT_INTERESTED"):
        status = "OPEN_TO_LISTEN"

    candidate = {
        "candidateId": cid,
        "name": body.get("name", ""),
        "dni": body.get("dni", ""),
        "role": body.get("role", ""),
        "location": body.get("location", ""),
        "status": status,
        "experience": body.get("experience"),
        "strength": body.get("strength", ""),
        "salaryRange": body.get("salaryRange", ""),
        "notes": body.get("notes", ""),
        "createdAt": now,
    }
    candidates_table.put_item(Item=candidate)
    return 201, candidate


# GET /candidates/{candidate_id}
def get_candidate_service(event, candidate_id: str):
    resp = candidates_table.get_item(Key={"candidateId": candidate_id})
    c = resp.get("Item")
    if not c:
        return 404, {"error": "not_found"}
    return 200, c


# PATCH /candidates/{candidate_id}
def update_candidate_service(event, candidate_id: str):
    resp = candidates_table.get_item(Key={"candidateId": candidate_id})
    c = resp.get("Item")
    if not c:
        return 404, {"error": "not_found"}

    body_raw = event.get("body") or "{}"
    body = json.loads(body_raw)

    for k, v in body.items():
        c[k] = v
    c["updatedAt"] = datetime.utcnow().isoformat()

    candidates_table.put_item(Item=c)
    return 200, c


# DELETE /candidates/{candidate_id}
def delete_candidate_service(event, candidate_id: str):
    headers = event.get("headers") or {}
    headers_lower = {k.lower(): v for k, v in headers.items()}
    role = headers_lower.get("x-role", "recruiter")

    if role != "admin":
        return 403, {"error": "forbidden"}

    # comprobamos que exista
    resp = candidates_table.get_item(Key={"candidateId": candidate_id})
    if "Item" not in resp:
        return 404, {"error": "not_found"}

    candidates_table.delete_item(Key={"candidateId": candidate_id})
    return 200, {"deleted": candidate_id}
