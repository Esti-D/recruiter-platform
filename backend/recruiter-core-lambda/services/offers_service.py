import json
from datetime import datetime
import uuid

from models.store import offers_table  # ahora usamos la tabla de DynamoDB


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


# GET /offers
def list_offers_service(event):
    params = event.get("queryStringParameters") or {}

    q = params.get("q")
    company_name = params.get("companyName")
    contact_person = params.get("contactPerson")
    role = params.get("role")
    modality = params.get("modality")
    location = params.get("location")

    def matches(o: dict):
        if q and not any(
            _m(q) in _m(str(o.get(k, "")))
            for k in ("companyName", "role", "description")
        ):
            return False
        if company_name and _m(company_name) != _m(o.get("companyName")):
            return False
        if contact_person and _m(contact_person) != _m(o.get("contactPerson")):
            return False
        if role and _m(role) != _m(o.get("role")):
            return False
        if modality and _m(modality) != _m(o.get("modality")):
            return False
        if location and _m(location) != _m(o.get("location")):
            return False
        return True

    items = _scan_all(offers_table)
    data = [v for v in items if matches(v)]
    return 200, data


# POST /offers
def create_offer_service(event):
    body_raw = event.get("body") or "{}"
    body = json.loads(body_raw)

    offer_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()

    offer = {
        "offerId": offer_id,
        "companyName": body.get("companyName", ""),
        "contactPerson": body.get("contactPerson", ""),
        "role": body.get("role", ""),
        "modality": body.get("modality", ""),
        "location": body.get("location", ""),
        "description": body.get("description", ""),
        "createdAt": now,
        "updatedAt": now,
    }

    offers_table.put_item(Item=offer)
    return 201, offer


# GET /offers/{offer_id}
def get_offer_service(event, offer_id: str):
    resp = offers_table.get_item(Key={"offerId": offer_id})
    offer = resp.get("Item")
    if not offer:
        return 404, {"error": "not_found"}
    return 200, offer


# PATCH /offers/{offer_id}
def update_offer_service(event, offer_id: str):
    resp = offers_table.get_item(Key={"offerId": offer_id})
    offer = resp.get("Item")
    if not offer:
        return 404, {"error": "not_found"}

    body_raw = event.get("body") or "{}"
    body = json.loads(body_raw)

    for k, v in body.items():
        offer[k] = v
    offer["updatedAt"] = datetime.utcnow().isoformat()

    offers_table.put_item(Item=offer)
    return 200, offer


# DELETE /offers/{offer_id}
def delete_offer_service(event, offer_id: str):
    headers = event.get("headers") or {}
    headers_lower = {k.lower(): v for k, v in headers.items()}
    role = headers_lower.get("x-role", "recruiter")

    if role != "admin":
        return 403, {"error": "forbidden"}

    # comprobamos que existe
    resp = offers_table.get_item(Key={"offerId": offer_id})
    if "Item" not in resp:
        return 404, {"error": "not_found"}

    offers_table.delete_item(Key={"offerId": offer_id})
    return 200, {"deleted": offer_id}
