from handler import lambda_handler
import json

# Simula POST /process
event = {
    "rawPath": "/process",
    "requestContext": {
        "http": {
            "method": "POST"
        }
    },
    "body": json.dumps({
        "offerId": "1",          # existe en models.store
        "recruiter": "esti",
        "notes": "Proceso de prueba"
    })
}

response = lambda_handler(event, None)
print(response)
