from datetime import datetime

PROCESSES = {}

OFFERS = {
    "1": {
        "offerId": "1",
        "companyName": "Empresa Demo",
        "contactPerson": "Pepe",
        "role": "Developer",
        "modality": "Remote",
        "location": "Bilbao",
        "description": "Oferta de prueba",
        "createdAt": datetime.utcnow().isoformat(),
    }
}

CANDIDATES = {
    "1": {
        "candidateId": "1",
        "name": "Ana Ejemplo",
        "dni": "12345678A",
        "role": "Developer",
        "location": "Bilbao",
        "status": "OPEN",
        "experience": 5,
        "strength": "Backend fuerte",
        "salaryRange": "40k-45k",
        "notes": "Candidata de prueba",
        "createdAt": datetime.utcnow().isoformat(),
    }
}
