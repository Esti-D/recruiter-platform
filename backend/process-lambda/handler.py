import json

from services.process_service import (
    create_process_service,
    list_processes_service,
    get_process_service,
    update_process_service,
    generate_candidates_service,
)


def lambda_handler(event, context):
    route = event.get("rawPath", "") or ""
    method = event.get("requestContext", {}).get("http", {}).get("method", "")

    status = 404
    body = {"error": "not_found"}

    # ---------------------------
    # /process
    # ---------------------------
    if route == "/process":
        if method == "POST":
            status, body = create_process_service(event)
        elif method == "GET":
            status, body = list_processes_service(event)
        else:
            status, body = 405, {"error": "method_not_allowed"}

    # ---------------------------
    # /process/{pid} y /process/{pid}/candidates:generate
    # ---------------------------
    elif route.startswith("/process/"):
        parts = route.split("/")  # ["", "process", "{pid}", ...]
        if len(parts) >= 3:
            pid = parts[2]

            # /process/{pid}
            if len(parts) == 3:
                if method == "GET":
                    status, body = get_process_service(event, pid)
                elif method == "PATCH":
                    status, body = update_process_service(event, pid)
                else:
                    status, body = 405, {"error": "method_not_allowed"}

            # /process/{pid}/candidates:generate
            elif len(parts) == 4 and parts[3] == "candidates:generate":
                if method == "POST":
                    status, body = generate_candidates_service(event, pid)
                else:
                    status, body = 405, {"error": "method_not_allowed"}
            else:
                status, body = 404, {"error": "not_found"}
        else:
            status, body = 404, {"error": "not_found"}

    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(body, default=str),
    }
