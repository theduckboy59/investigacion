from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI

from app.routers.aulas import router as aulas_router
from app.routers.horarios import router as horarios_router

# Carga backend/.env si existe.
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

app = FastAPI(
    title="Horarios Inteligentes",
    description="API para la gestión y optimización de horarios académicos",
    version="1.0.0",
)


# Endpoint principal para comprobar que la API funciona.
@app.get("/")
def inicio():
    return {
        "mensaje": "API de Horarios Inteligentes funcionando"
    }


# Registrar las rutas de los módulos.
app.include_router(aulas_router)
app.include_router(horarios_router)
