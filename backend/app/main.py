
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI

# Carga backend/.env si existe.
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

from app.routers.horarios import router as horarios_router

app = FastAPI(
    title="Horarios Inteligentes",
    description="API para la generación y optimización de horarios académicos",
    version="1.0.0"
)

app.include_router(horarios_router)


@app.get("/")
def inicio():
    return {
        "mensaje": "API de Horarios Inteligentes funcionando"
    }
