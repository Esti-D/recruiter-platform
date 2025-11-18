import json
from datetime import datetime
import uuid

from models.store import PROCESSES, OFFERS, CANDIDATES


# POST /process
def create_process_service(event):
    body_raw = event.get("body") or "{}"
    body = json.loads(body_raw)

    offer_id = body.get("offerId")
    recruiter = body.get("recruiter")
    notes = body.get("notes")

    # Buscar oferta por offerId
    off = next((v for v in OFFERS.values() if v.get("offerId") == offer_id), None)
    if not off:
        return 404, {"error": "offer_not_found"}

    pid = str(uuid.uuid4())

    p = {
        "processId": pid,
        "offerId": offer_id,
        "roleOffer": off.get("role"),
        "similarRoles": [],
        "recruiter": recruiter,
        "notes": notes,
        "status": "OPEN",
        "createdAt": datetime.utcnow().isoformat(),
        "closedAt": None,
        "candidates": [],
    }

    PROCESSES[pid] = p
    return 201, p


# GET /process
def list_processes_service(event):
    params = event.get("queryStringParameters") or {}

    offer_id = params.get("offerId")
    status_filter = params.get("status")

    def ok(x: dict):
        if offer_id and x.get("offerId") != offer_id:
            return False
        if status_filter and x.get("status") != status_filter:
            return False
        return True

    data = [v for v in PROCESSES.values() if ok(v)]
    return 200, data


# GET /process/{pid}
def get_process_service(event, pid: str):
    p = PROCESSES.get(pid)
    if not p:
        return 404, {"error": "not_found"}
    return 200, p


# PATCH /process/{pid}
def update_process_service(event, pid: str):
    p = PROCESSES.get(pid)
    if not p:
        return 404, {"error": "not_found"}

    body_raw = event.get("body") or "{}"
    body = json.loads(body_raw)

    # actualizar campos simples
    for k, v in body.items():
        p[k] = v

    # si se cierra el proceso y no tiene closedAt, lo ponemos ahora
    if p.get("status") == "CLOSED" and not p.get("closedAt"):
        p["closedAt"] = datetime.utcnow().isoformat()

    return 200, p


# POST /process/{pid}/candidates:generate
def generate_candidates_service(event, pid: str):
    p = PROCESSES.get(pid)
    if not p:
        return 404, {"error": "not_found"}

    body_raw = event.get("body") or "{}"
    payload = json.loads(body_raw)

    similar_roles = payload.get("similarRoles", []) or []

    # Conjunto de roles a usar
    roles = {p.get("roleOffer"), *similar_roles}

    # Seleccionar candidatos aptos
    selected = [
        c for c in CANDIDATES.values()
        if c.get("status", "OPEN") == "OPEN" and c.get("role") in roles
    ]

    p["similarRoles"] = similar_roles

    # Formato candidatos dentro del proceso
    candidates_in_process = []
    for c in selected:
        candidates_in_process.append({
            "candidateId": c.get("candidateId"),
            "name": c.get("name"),
            "role": c.get("role"),
            "experience": c.get("experience"),
            "strength": c.get("strength"),
            "salaryRange": c.get("salaryRange"),
        })

    p["candidates"] = candidates_in_process

    return 200, {
        "processId": pid,
        "count": len(p["candidates"]),
    }
