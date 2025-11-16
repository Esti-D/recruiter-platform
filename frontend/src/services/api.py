import os, requests, uuid
from dotenv import load_dotenv
load_dotenv()
BASE_URL = os.getenv("API_BASE", "http://127.0.0.1:8000")
USER_ROLE = os.getenv("USER_ROLE", "recruiter")
HDR = {"X-Role": USER_ROLE}

# ============================================================
# PROCESS
# ============================================================

def create_process(offer_id, recruiter=None, notes=None):
    """
    Crea un proceso (POST /process).
    El backend genera processId, createdAt, etc.
    """
    payload = {
        "offerId": offer_id,
        "recruiter": recruiter,
        "notes": notes,
    }
    r = requests.post(f"{BASE_URL}/process", json=payload, headers=HDR)
    r.raise_for_status()
    return r.json()


def get_process(process_id):
    """
    Devuelve el detalle de un proceso (GET /process/{id}).
    """
    r = requests.get(f"{BASE_URL}/process/{process_id}", headers=HDR)
    r.raise_for_status()
    return r.json()


def list_processes(status=None, offer_id=None):
    """
    Lista procesos (GET /process) con filtros opcionales.
    """
    params = {}
    if status:
        params["status"] = status
    if offer_id:
        params["offerId"] = offer_id

    r = requests.get(f"{BASE_URL}/process", params=params, headers=HDR)
    r.raise_for_status()
    return r.json()


def update_process(process_id, changes: dict):
    """
    Actualiza un proceso (PATCH /process/{id}).
    Útil para cambiar status, notes, candidates[], etc.
    """
    r = requests.patch(
        f"{BASE_URL}/process/{process_id}",
        json=changes,
        headers=HDR,
    )
    r.raise_for_status()
    return r.json()


def delete_process(process_id):
    """
    Elimina un proceso (DELETE /process/{id}).
    Depende de las reglas de permisos del backend.
    """
    r = requests.delete(f"{BASE_URL}/process/{process_id}", headers=HDR)
    r.raise_for_status()
    # el backend puede devolver o no body; devolvemos json si existe
    try:
        return r.json()
    except ValueError:
        return None


def generate_candidates(process_id, similar_roles: list[str]):
    """
    Genera la lista de candidatos para un proceso:
    POST /process/{id}/candidates:generate
    Body: {"similarRoles": [...]}
    """
    payload = {"similarRoles": similar_roles}
    r = requests.post(
        f"{BASE_URL}/process/{process_id}/candidates:generate",
        json=payload,
        headers=HDR,
    )
    r.raise_for_status()
    return r.json()

# ============================================================
# CANDIDATES
# ============================================================

def get_candidates(role=None, skills=None, status=None):
    """
    Lista candidatos (GET /candidates) con filtros opcionales.
    role / skills dependen de lo que soporte tu backend.
    """
    params = {}
    if role:
        params["role"] = role
    if skills:
        params["skills"] = skills
    if status:
        params["status"] = status

    r = requests.get(f"{BASE_URL}/candidates", params=params, headers=HDR)
    r.raise_for_status()
    return r.json()


def create_candidate(data: dict):
    """
    Crea un candidato (POST /candidates).
    El backend genera candidateId, createdAt.
    """
    r = requests.post(f"{BASE_URL}/candidates", json=data, headers=HDR)
    r.raise_for_status()
    return r.json()


def get_candidate(candidate_id: str):
    """
    Detalle de un candidato (GET /candidates/{id}).
    """
    r = requests.get(f"{BASE_URL}/candidates/{candidate_id}", headers=HDR)
    r.raise_for_status()
    return r.json()


def update_candidate(candidate_id: str, changes: dict):
    """
    Actualiza un candidato (PATCH /candidates/{id}).
    """
    r = requests.patch(
        f"{BASE_URL}/candidates/{candidate_id}",
        json=changes,
        headers=HDR,
    )
    r.raise_for_status()
    return r.json()


def delete_candidate(candidate_id: str):
    """
    Elimina un candidato (DELETE /candidates/{id}).
    Normalmente restringido a rol admin.
    """
    r = requests.delete(f"{BASE_URL}/candidates/{candidate_id}", headers=HDR)
    r.raise_for_status()
    try:
        return r.json()
    except ValueError:
        return None


# --- OFFERS ---
def create_offer(data: dict):
    """
    Crea una oferta con el modelo definitivo.
    Los campos automáticos (offerId, createdAt, updatedAt) los genera el backend.
    """
    r = requests.post(f"{BASE_URL}/offers", json=data, headers=HDR)
    r.raise_for_status()
    return r.json()


def list_offers(q=None, role=None, company=None):
    params={}; 
    if q: params["q"]=q
    if role: params["role"]=role
    if company: params["companyName"]=company
    r=requests.get(f"{BASE_URL}/offers",params=params,headers=HDR); r.raise_for_status(); return r.json()

def get_offer(offer_id):
    r=requests.get(f"{BASE_URL}/offers/{offer_id}",headers=HDR); r.raise_for_status(); return r.json()

def update_offer(offer_id, changes:dict):
    r=requests.patch(f"{BASE_URL}/offers/{offer_id}",json=changes,headers=HDR); r.raise_for_status(); return r.json()

def delete_offer(offer_id):
    r=requests.delete(f"{BASE_URL}/offers/{offer_id}",headers=HDR); r.raise_for_status(); return r.json()


def list_roles(q=None):
    params = {}
    if q:
        params["q"] = q
    r = requests.get(f"{BASE_URL}/roles", params=params, headers=HDR)
    r.raise_for_status()
    return r.json()

def create_role(name: str):
    r = requests.post(f"{BASE_URL}/roles", json={"name": name}, headers=HDR)
    r.raise_for_status()
    return r.json()

def update_role(role_id: str, name: str):
    r = requests.patch(f"{BASE_URL}/roles/{role_id}", json={"name": name}, headers=HDR)
    r.raise_for_status()
    return r.json()

def delete_role(role_id: str):
    r = requests.delete(f"{BASE_URL}/roles/{role_id}", headers=HDR)
    r.raise_for_status()
    return r.json()

def reassign_role(old_role_id: str, new_role_id: str):
    r = requests.post(
        f"{BASE_URL}/roles/{old_role_id}/reassign",
        json={"newRoleId": new_role_id},
        headers=HDR
    )
    r.raise_for_status()
    return r.json()
