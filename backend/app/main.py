
from fastapi import FastAPI
from app.routers.aulas import router as aulas_router

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


# Registrar las rutas del módulo de aulas.
app.include_router(aulas_router)
