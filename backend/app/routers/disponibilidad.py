
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.disponibilidad import (
    DisponibilidadResponse,
    DisponibilidadUpdate,
)
from app.services import disponibilidad_service


router = APIRouter(
    prefix="/api/catedraticos",
    tags=["Disponibilidad docente"]
)


@router.get(
    "/{id_profesor}/disponibilidad",
    response_model=list[DisponibilidadResponse]
)
def consultar(
    id_profesor: int,
    db: Session = Depends(get_db)
):
    return disponibilidad_service.obtener_disponibilidad(
        db, id_profesor
    )


@router.put(
    "/{id_profesor}/disponibilidad",
    response_model=list[DisponibilidadResponse]
)
def actualizar(
    id_profesor: int,
    datos: DisponibilidadUpdate,
    db: Session = Depends(get_db)
):
    return disponibilidad_service.actualizar_disponibilidad(
        db, id_profesor, datos
    )
