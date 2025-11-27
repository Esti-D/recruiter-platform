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
        "Access-Control-Allow-Headers": "Content-Type,Authorization,X-Requested-With,X-Api-Key",
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


def lambda_handler(event, context):
    # 👀 Log para ver qué nos llega exactamente:
    logger.info("EVENT: %s", json.dumps(event))

    # Soporta HTTP API v2 (rawPath/http.method) y REST API (path/httpMethod)
    route = event.get("rawPath") or event.get("path") or ""
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

            else:
                return _response(404, {"error": "not_found"})

        return _response(404, {"error": "not_found"})

    # ---------------------------
    # DEFAULT
    # ---------------------------
    return _response(404, {"error": "not_found"})
