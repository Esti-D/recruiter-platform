from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_offers():
    return {"service": "process", "status": "ok"}
