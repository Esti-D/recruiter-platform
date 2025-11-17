from datetime import datetime

CANDIDATES = {
    "1": {
        "candidateId": "1",
        "name": "Ana Ejemplo",
        "dni": "12345678A",
        "role": "Developer",
        "location": "Bilbao",
        "status": "OPEN",
        "notes": "Candidata de prueba",
        "createdAt": datetime.utcnow().isoformat(),
    }
}

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

ROLES = {
    "1": {
        "roleId": "1",
        "name": "Developer",
        "createdAt": "2025-11-17T18:30:12"
    }
}