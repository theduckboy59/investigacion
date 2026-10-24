
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.optimizer.service import generar_horario

router = APIRouter(
    prefix="/api/horarios",
    tags=["Horarios"]
)


class GenerarHorarioRequest(BaseModel):
    periodo_id: int = Field(gt=0)


@router.post("/generar")
def generar(request: GenerarHorarioRequest):
    try:
        return generar_horario(request.periodo_id)

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        ) from error

    except Exception as error:
        # El detalle técnico se conserva en el servidor,
        # pero no se expone al cliente.
        print(f"Error al generar horario: {error}")

        raise HTTPException(
            status_code=500,
            detail=(
                "No fue posible generar el horario. "
                "Verifique la configuración y los registros de la base de datos."
            )
        ) from error
