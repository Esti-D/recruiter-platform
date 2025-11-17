from handler import lambda_handler

event = {
    "rawPath": "/candidates",
    "requestContext": {
        "http": {
            "method": "GET"
        }
    },
    "queryStringParameters": {
        "q": "Ana"   # puedes cambiar o quitar el filtro
    }
}

response = lambda_handler(event, None)
print(response)
