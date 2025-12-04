import json
import logging

from services.process_service import (
    create_process_service,
    list_processes_service,
    get_process_service,
    update_process_service,
    generate_candidates_service,
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def _cors_headers():
    return {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET,POST,PATCH,PUT,DELETE,OPTIONS",
        "Access-Control-Allow-Headers": (
            "Content-Type,Authorization,X-Requested-With,"
            "X-Api-Key,X-Role,X-User-Id"
        ),
    }



def _response(status: int, body):
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
    Igual que en recruiter-core-lambda:
    elimina el stage (/prod) del rawPath si viene incluido.
    """
    raw_path = (event.get("rawPath") or event.get("path") or "").strip() or "/"
    ctx = event.get("requestContext", {}) or {}
    stage = ctx.get("stage")

    if stage:
        prefix = f"/{stage}"
        if raw_path.startswith(prefix):
            raw_path = raw_path[len(prefix):] or "/"

    return raw_path


def lambda_handler(event, context):
    logger.info("EVENT: %s", json.dumps(event))

    route = _normalize_path(event)
    method = (
        event.get("requestContext", {})
        .get("http", {})
        .get("method", "")
        or event.get("httpMethod", "")
    )

    # ------ CORS PRE-FLIGHT ------
    if method == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": _cors_headers(),
            "body": "",
        }

    # ---------------------------
    # /processes  (lista + creación)
    # ---------------------------
    if route == "/processes":
        if method == "GET":
            status, body = list_processes_service(event)
        elif method == "POST":
            status, body = create_process_service(event)
        else:
            return _response(405, {"error": "method_not_allowed"})
        return _response(status, body)

    # ---------------------------
    # /processes/{pid} y /processes/{pid}/candidates:generate
    # ---------------------------
    if route.startswith("/processes/"):
        parts = route.split("/")  # ["", "processes", "{pid}", ...]
        if len(parts) >= 3:
            pid = parts[2]

            # /processes/{pid}
            if len(parts) == 3:
                if method == "GET":
                    status, body = get_process_service(event, pid)
                elif method == "PATCH":
                    status, body = update_process_service(event, pid)
                else:
                    return _response(405, {"error": "method_not_allowed"})
                return _response(status, body)

            # /processes/{pid}/candidates:generate
            elif len(parts) == 4 and parts[3] == "candidates:generate":
                if method == "POST":
                    status, body = generate_candidates_service(event, pid)
                else:
                    return _response(405, {"error": "method_not_allowed"})
                return _response(status, body)

        return _response(404, {"error": "not_found"})

    # ---------------------------
    # DEFAULT
    # ---------------------------
    return _response(404, {"error": "not_found"})
