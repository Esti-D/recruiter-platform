import json

from services.candidates_service import (
    list_candidates_service,
    create_candidate_service,
    get_candidate_service,
    update_candidate_service,
    delete_candidate_service,
)

from services.offers_service import (
    list_offers_service,
    create_offer_service,
    get_offer_service,
    update_offer_service,
    delete_offer_service,
)

from services.roles_service import (
    list_roles_service,
    create_role_service,
    get_role_service,
    update_role_service,
    delete_role_service,
    reassign_role_service,
)


# ======================================================
# CORS HELPERS
# ======================================================
def _cors_headers():
    return {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET,POST,PATCH,PUT,DELETE,OPTIONS",
        "Access-Control-Allow-Headers": (
            "Content-Type,Authorization,X-Requested-With,"
            "X-Api-Key,X-Role,X-User-Id"
        ),
    }



def _response(status, body):
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            **_cors_headers(),
        },
        "body": json.dumps(body, default=str),
    }


def _normalize_path(event) -> str:
    """
    Normaliza el rawPath eliminando el stage si viene incluido
    (por ejemplo /prod/roles -> /roles).
    """
    raw_path = (event.get("rawPath") or "").strip() or "/"
    ctx = event.get("requestContext", {}) or {}
    stage = ctx.get("stage")

    # Si hay stage y el path empieza por /{stage}, lo quitamos
    if stage:
        prefix = f"/{stage}"
        if raw_path.startswith(prefix):
            raw_path = raw_path[len(prefix):] or "/"

    return raw_path


# ======================================================
# MAIN HANDLER
# ======================================================
def lambda_handler(event, context):
    route = _normalize_path(event)
    method = event.get("requestContext", {}).get("http", {}).get("method", "")

    # ------ CORS PRE-FLIGHT ------
    if method == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": _cors_headers(),
            "body": "",
        }

    # ---------------------------
    # CANDIDATES
    # ---------------------------
    if route == "/candidates":
        if method == "GET":
            status, body = list_candidates_service(event)
        elif method == "POST":
            status, body = create_candidate_service(event)
        else:
            return _response(405, {"error": "method_not_allowed"})
        return _response(status, body)

    elif route.startswith("/candidates/"):
        candidate_id = route.split("/")[-1]

        if method == "GET":
            status, body = get_candidate_service(event, candidate_id)
        elif method == "PATCH":
            status, body = update_candidate_service(event, candidate_id)
        elif method == "DELETE":
            status, body = delete_candidate_service(event, candidate_id)
        else:
            return _response(405, {"error": "method_not_allowed"})
        return _response(status, body)

    # ---------------------------
    # OFFERS
    # ---------------------------
    elif route == "/offers":
        if method == "GET":
            status, body = list_offers_service(event)
        elif method == "POST":
            status, body = create_offer_service(event)
        else:
            return _response(405, {"error": "method_not_allowed"})
        return _response(status, body)

    elif route.startswith("/offers/"):
        offer_id = route.split("/")[-1]

        if method == "GET":
            status, body = get_offer_service(event, offer_id)
        elif method == "PATCH":
            status, body = update_offer_service(event, offer_id)
        elif method == "DELETE":
            status, body = delete_offer_service(event, offer_id)
        else:
            return _response(405, {"error": "method_not_allowed"})
        return _response(status, body)

    # ---------------------------
    # ROLES
    # ---------------------------
    elif route == "/roles":
        if method == "GET":
            status, body = list_roles_service(event)
        elif method == "POST":
            status, body = create_role_service(event)
        else:
            return _response(405, {"error": "method_not_allowed"})
        return _response(status, body)

    elif route.startswith("/roles/"):
        parts = route.split("/")

        if len(parts) == 3:
            # /roles/{role_id}
            role_id = parts[2]

            if method == "GET":
                status, body = get_role_service(event, role_id)
            elif method == "PATCH":
                status, body = update_role_service(event, role_id)
            elif method == "DELETE":
                status, body = delete_role_service(event, role_id)
            else:
                return _response(405, {"error": "method_not_allowed"})
            return _response(status, body)

        elif len(parts) == 4 and parts[3] == "reassign":
            # /roles/{role_id}/reassign
            role_id = parts[2]

            if method == "POST":
                status, body = reassign_role_service(event, role_id)
            else:
                return _response(405, {"error": "method_not_allowed"})
            return _response(status, body)

        else:
            return _response(404, {"error": "not_found"})
        
    # ---------------------------
    # WORKFLOW (solo recruiter)
    # ---------------------------
    elif route == "/workflow/candidates" and method == "GET":
        status, body = list_candidates_service(event, workflow_only="CREATED")
        return _response(status, body)

    elif route == "/workflow/offers" and method == "GET":
        status, body = list_offers_service(event, workflow_only="CREATED")
        return _response(status, body)
    
    # ---------------------------
    # DEFAULT
    # ---------------------------
    return _response(404, {"error": "not_found"})
