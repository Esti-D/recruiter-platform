from handler import lambda_handler

# primero probamos lista vacía de procesos
event = {
    "rawPath": "/process",
    "requestContext": {
        "http": {
            "method": "GET"
        }
    },
    "queryStringParameters": {}
}

response = lambda_handler(event, None)
print(response)
