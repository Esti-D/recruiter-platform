from handler import lambda_handler

# Evento que simula GET /offers
event = {
    "rawPath": "/offers",
    "requestContext": {
        "http": {
            "method": "GET"
        }
    },
    "queryStringParameters": {
        # Puedes usar este filtro o dejarlo vacío:
        # "q": "Developer"
    }
}

response = lambda_handler(event, None)
print(response)
