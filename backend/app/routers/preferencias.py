
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.preferencia import (
    PreferenciaResponse,
    PreferenciaUpdate,
)
from app.services import preferencia_service


router = APIRouter(
    prefix="/api/catedraticos",
    tags=["Preferencias docentes"]
)


@router.get(
    "/{id_profesor}/preferencias",
    response_model=list[PreferenciaResponse]
)
def consultar(
    id_profesor: int,
    db: Session = Depends(get_db)
):
    return preferencia_service.obtener_preferencias(
        db, id_profesor
    )


@router.put(
    "/{id_profesor}/preferencias",
    response_model=list[PreferenciaResponse]
)
def actualizar(
    id_profesor: int,
    datos: PreferenciaUpdate,
    db: Session = Depends(get_db)
):
    return preferencia_service.actualizar_preferencias(
        db, id_profesor, datos
    )
