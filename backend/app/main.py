from fastapi import FastAPI

app = FastAPI(
    title="Horarios Inteligentes",
    description="API para la gestión y optimización de horarios académicos",
    version="1.0.0"
)

@app.get("/")
def inicio():
    return {
        "mensaje": "API de Horarios Inteligentes funcionando"
    }