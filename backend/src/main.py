from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.offers.router import router as offers_router
from src.process.router import router as process_router
from src.candidates.router import router as candidates_router
app = FastAPI(); app.include_router(offers_router, prefix="/offers")
from src.roles.router import router as roles_router
app.include_router(roles_router, prefix="/roles")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # luego pondremos la URL real del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(process_router, prefix="/process")
app.include_router(candidates_router, prefix="/candidates")

@app.get("/")
def root():
    return {"status": "ok", "version": "v1.0-desktop"}
