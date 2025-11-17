import json
from datetime import datetime
import uuid

from models.store import CANDIDATES


def _m(v):
    return v.lower() if isinstance(v, str) else v


# GET /candidates
def list_candidates_service(event):
    params = event.get("queryStringParameters") or {}

    q = params.get("q")
    role = params.get("role")
    location = params.get("location")
    status = params.get("status")

    def ok(c):
        if q and not any(_m(q) in _m(str(c.get(k, ""))) for k in ("name", "dni", "role", "location", "notes")):
            return False
        if role and _m(role) != _m(c.get("role")):
            return False
        if location and _m(location) != _m(c.get("location")):
            return False
        if status and _m(status) != _m(c.get("status")):
            return False
        return True

    data = [v for v in CANDIDATES.values() if ok(v)]
    return 200, data


# POST /candidates
def create_candidate_service(event):
    body_raw = event.get("body") or "{}"
    body = json.loads(body_raw)

    cid = str(uuid.uuid4())
    candidate = body | {
        "candidateId": cid,
        "createdAt": datetime.utcnow().isoformat()
    }
    CANDIDATES[cid] = candidate
    return 201, candidate


# GET /candidates/{candidate_id}
def get_candidate_service(event, candidate_id: str):
    c = CANDIDATES.get(candidate_id)
    if not c:
        return 404, {"error": "not_found"}
    return 200, c


# PATCH /candidates/{candidate_id}
def update_candidate_service(event, candidate_id: str):
    c = CANDIDATES.get(candidate_id)
    if not c:
        return 404, {"error": "not_found"}

    body_raw = event.get("body") or "{}"
    body = json.loads(body_raw)

    for k, v in body.items():
        c[k] = v
    c["updatedAt"] = datetime.utcnow().isoformat()
    return 200, c


# DELETE /candidates/{candidate_id}
def delete_candidate_service(event, candidate_id: str):
    headers = event.get("headers") or {}
    # normalizamos a minúsculas
    headers_lower = {k.lower(): v for k, v in headers.items()}
    role = headers_lower.get("x-role", "recruiter")

    if role != "admin":
        return 403, {"error": "forbidden"}

    if candidate_id not in CANDIDATES:
        return 404, {"error": "not_found"}

    CANDIDATES.pop(candidate_id)
    return 200, {"deleted": candidate_id}
