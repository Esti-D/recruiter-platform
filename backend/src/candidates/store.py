from datetime import datetime

_initial_candidates = [
    {
        "candidateId": "1",
        "dni": "11111111A",
        "name": "Ana",
        "role": "Backend",
        "experience": None,
        "location": "Bilbao",
        "email": "ana@example.com",
        "phone": None,
        "status": "OPEN",
        "strength": None,
        "salaryRange": None,
        "notes": None,
        "createdAt": datetime.utcnow(),
    },
    {
        "candidateId": "2",
        "dni": "22222222B",
        "name": "Luis",
        "role": "Frontend",
        "experience": None,
        "location": "Bilbao",
        "email": "luis@example.com",
        "phone": None,
        "status": "OPEN",
        "strength": None,
        "salaryRange": None,
        "notes": None,
        "createdAt": datetime.utcnow(),
    },
    {
        "candidateId": "3",
        "dni": "000003C",
        "name": "Marta",
        "role": "DevOps",
        "experience": None,
        "location": "Bilbao",
        "email": "marta@example.com",
        "phone": None,
        "status": "OPEN",
        "strength": None,
        "salaryRange": None,
        "notes": None,
        "createdAt": datetime.utcnow(),
    },
]

# Simulación tipo “tabla Dynamo”: clave = candidateId, valor = dict
CANDIDATES = {c["candidateId"]: c for c in _initial_candidates}