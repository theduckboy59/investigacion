
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.ciclo import (
    CicloCreate,
    CicloUpdate,
    CicloResponse,
)
from app.services import ciclo_service


router = APIRouter(
    prefix="/api/ciclos",
    tags=["Ciclos"]
)


@router.get("", response_model=list[CicloResponse])
def listar(db: Session = Depends(get_db)):
    return ciclo_service.listar_ciclos(db)


@router.get("/{ciclo_id}", response_model=CicloResponse)
def obtener(
    ciclo_id: int,
    db: Session = Depends(get_db)
):
    ciclo = ciclo_service.obtener_ciclo(db, ciclo_id)

    if ciclo is None:
        raise HTTPException(
            status_code=404,
            detail="Ciclo no encontrado"
        )

    return ciclo


@router.post(
    "",
    response_model=CicloResponse,
    status_code=201
)
def crear(
    datos: CicloCreate,
    db: Session = Depends(get_db)
):
    return ciclo_service.crear_ciclo(db, datos)


@router.put(
    "/{ciclo_id}",
    response_model=CicloResponse
)
def actualizar(
    ciclo_id: int,
    datos: CicloUpdate,
    db: Session = Depends(get_db)
):
    ciclo = ciclo_service.actualizar_ciclo(
        db, ciclo_id, datos
    )

    if ciclo is None:
        raise HTTPException(
            status_code=404,
            detail="Ciclo no encontrado"
        )

    return ciclo


@router.delete("/{ciclo_id}", status_code=204)
def eliminar(
    ciclo_id: int,
    db: Session = Depends(get_db)
):
    eliminado = ciclo_service.eliminar_ciclo(
        db, ciclo_id
    )

    if not eliminado:
        raise HTTPException(
            status_code=404,
            detail="Ciclo no encontrado"
        )
