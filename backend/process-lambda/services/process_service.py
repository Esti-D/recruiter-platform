import json
import os
from datetime import datetime
import uuid

import boto3

# DynamoDB
dynamo = boto3.resource("dynamodb")
processes_table = dynamo.Table(os.environ["PROCESSES_TABLE"])
candidates_table = dynamo.Table(os.environ["CANDIDATES_TABLE"])


def _now_iso() -> str:
    return datetime.utcnow().isoformat()


def _process_from_item(item: dict) -> dict:
    # Aquí podrías normalizar tipos si hiciera falta
    return item


# ======================================================
# POST /processes
# (creación manual de un proceso)
# ======================================================
def create_process_service(event):
    body_raw = event.get("body") or "{}"
    body = json.loads(body_raw)

    offer_id = body.get("offerId")
    recruiter = body.get("recruiter", "")
    notes = body.get("notes", "")
    role_offer = body.get("roleOffer") or body.get("role")

    if not offer_id:
        return 400, {"error": "offerId_required"}
    if not role_offer:
        return 400, {"error": "roleOffer_required"}

    pid = str(uuid.uuid4())

    item = {
        "processId": pid,
        "offerId": offer_id,
        "roleOffer": role_offer,
        "similarRoles": body.get("similarRoles", []) or [],
        "recruiter": recruiter,
        "notes": notes,
        # Estado del PROCESO (no del candidato)
        "status": "OPEN",
        "createdAt": _now_iso(),
        "closedAt": None,
        # Lista de candidatos embebida en el proceso
        "candidates": [],
    }

    processes_table.put_item(Item=item)

    return 201, _process_from_item(item)


# ======================================================
# GET /processes
# ======================================================
def list_processes_service(event):
    params = event.get("queryStringParameters") or {}

    offer_id = params.get("offerId")
    status_filter = params.get("status")

    resp = processes_table.scan()
    items = resp.get("Items", [])

    def ok(x: dict) -> bool:
        if offer_id and x.get("offerId") != offer_id:
            return False
        if status_filter and x.get("status") != status_filter:
            return False
        return True

    data = [_process_from_item(v) for v in items if ok(v)]
    return 200, data


# ======================================================
# GET /processes/{pid}
# ======================================================
def get_process_service(event, pid: str):
    resp = processes_table.get_item(Key={"processId": pid})
    item = resp.get("Item")
    if not item:
        return 404, {"error": "not_found"}
    return 200, _process_from_item(item)


# ======================================================
# PATCH /processes/{pid}
# ======================================================
def update_process_service(event, pid: str):
    body_raw = event.get("body") or "{}"
    body = json.loads(body_raw)

    resp = processes_table.get_item(Key={"processId": pid})
    item = resp.get("Item")
    if not item:
        return 404, {"error": "not_found"}

    # Actualizar campos (puede venir también la lista "candidates")
    for k, v in body.items():
        item[k] = v

    # Si el proceso se marca CLOSED y no tenía closedAt, lo rellenamos
    if item.get("status") == "CLOSED" and not item.get("closedAt"):
        item["closedAt"] = _now_iso()

    processes_table.put_item(Item=item)

    return 200, _process_from_item(item)


# ======================================================
# POST /processes/{pid}/candidates:generate
# ======================================================
def generate_candidates_service(event, pid: str):
    # 1) Cargar proceso
    resp = processes_table.get_item(Key={"processId": pid})
    item = resp.get("Item")
    if not item:
        return 404, {"error": "not_found"}

    body_raw = event.get("body") or "{}"
    payload = json.loads(body_raw)

    similar_roles = payload.get("similarRoles", []) or []

    # Conjunto de roles: rol principal de la oferta + similares
    roles = {item.get("roleOffer")}
    roles.update([r for r in similar_roles if r])

    # 2) Leer candidatos de Dynamo y filtrar
    cand_resp = candidates_table.scan()
    all_candidates = cand_resp.get("Items", [])

    selected = []
    for c in all_candidates:
        # Estado GLOBAL del candidato:
        # sólo queremos los que estén abiertos a escuchar
        status = c.get("status")
        if status != "OPEN_TO_LISTEN":
            continue

        # Debe encajar por rol
        if c.get("role") not in roles:
            continue

        selected.append(c)

    # Guardamos similarRoles usados en este proceso
    item["similarRoles"] = similar_roles

    # 3) Construir lista de candidatos del proceso
    candidates_in_process = []
    for c in selected:
        candidates_in_process.append(
            {
                # Datos que vienen del perfil del candidato
                "candidateId": c.get("candidateId"),
                "name": c.get("name"),
                "role": c.get("role"),
                "experience": c.get("experience"),
                "strength": c.get("strength"),
                "salaryRange": c.get("salaryRange"),

                # Datos específicos de ESTE proceso
                # (estado del candidato en este proceso)
                "processStatus": "INITIAL",  # se editará desde la UI
                "processNotes": "",          # notas del recruiter en este proceso
            }
        )

    item["candidates"] = candidates_in_process

    # 4) Guardar en DynamoDB
    processes_table.put_item(Item=item)

    return 200, {
        "processId": pid,
        "count": len(candidates_in_process),
    }
