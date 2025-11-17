from handler import lambda_handler

# Evento que simula GET /roles
event = {
    "rawPath": "/roles",
    "requestContext": {
        "http": {
            "method": "GET"
        }
    },
    "queryStringParameters": {
        # "q": "Dev"   # si quieres probar filtro por nombre
    }
}

response = lambda_handler(event, None)
print(response)
