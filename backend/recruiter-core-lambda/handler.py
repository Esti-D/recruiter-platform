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


def lambda_handler(event, context):
    route = event.get("rawPath", "") or ""
    method = event.get("requestContext", {}).get("http", {}).get("method", "")

    status = 404
    body = {"error": "not_found"}

    # ---------------------------
    # CANDIDATES
    # ---------------------------
    if route == "/candidates":
        if method == "GET":
            status, body = list_candidates_service(event)
        elif method == "POST":
            status, body = create_candidate_service(event)
        else:
            status, body = 405, {"error": "method_not_allowed"}

    elif route.startswith("/candidates/"):
        candidate_id = route.split("/")[-1]

        if method == "GET":
            status, body = get_candidate_service(event, candidate_id)
        elif method == "PATCH":
            status, body = update_candidate_service(event, candidate_id)
        elif method == "DELETE":
            status, body = delete_candidate_service(event, candidate_id)
        else:
            status, body = 405, {"error": "method_not_allowed"}

    # ---------------------------
    # OFFERS
    # ---------------------------
    elif route == "/offers":
        if method == "GET":
            status, body = list_offers_service(event)
        elif method == "POST":
            status, body = create_offer_service(event)
        else:
            status, body = 405, {"error": "method_not_allowed"}

    elif route.startswith("/offers/"):
        offer_id = route.split("/")[-1]

        if method == "GET":
            status, body = get_offer_service(event, offer_id)
        elif method == "PATCH":
            status, body = update_offer_service(event, offer_id)
        elif method == "DELETE":
            status, body = delete_offer_service(event, offer_id)
        else:
            status, body = 405, {"error": "method_not_allowed"}

    # ---------------------------
    # ROLES
    # ---------------------------
    elif route == "/roles":
        if method == "GET":
            status, body = list_roles_service(event)
        elif method == "POST":
            status, body = create_role_service(event)
        else:
            status, body = 405, {"error": "method_not_allowed"}

    elif route.startswith("/roles/"):
        parts = route.split("/")  # ["", "roles", "{id}"] o ["", "roles", "{id}", "reassign"]

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
                status, body = 405, {"error": "method_not_allowed"}

        elif len(parts) == 4 and parts[3] == "reassign":
            # /roles/{role_id}/reassign
            role_id = parts[2]

            if method == "POST":
                status, body = reassign_role_service(event, role_id)
            else:
                status, body = 405, {"error": "method_not_allowed"}

        else:
            status, body = 404, {"error": "not_found"}

    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(body, default=str),
    }
