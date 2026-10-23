
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.carrera import (
    CarreraCreate,
    CarreraUpdate,
    CarreraResponse,
)
from app.services import carrera_service


router = APIRouter(
    prefix="/api/carreras",
    tags=["Carreras"]
)


@router.get("", response_model=list[CarreraResponse])
def listar(db: Session = Depends(get_db)):
    return carrera_service.listar_carreras(db)


@router.get("/{carrera_id}", response_model=CarreraResponse)
def obtener(
    carrera_id: int,
    db: Session = Depends(get_db)
):
    carrera = carrera_service.obtener_carrera(
        db, carrera_id
    )

    if carrera is None:
        raise HTTPException(
            status_code=404,
            detail="Carrera no encontrada"
        )

    return carrera


@router.post(
    "",
    response_model=CarreraResponse,
    status_code=201
)
def crear(
    datos: CarreraCreate,
    db: Session = Depends(get_db)
):
    return carrera_service.crear_carrera(db, datos)


@router.put(
    "/{carrera_id}",
    response_model=CarreraResponse
)
def actualizar(
    carrera_id: int,
    datos: CarreraUpdate,
    db: Session = Depends(get_db)
):
    carrera = carrera_service.actualizar_carrera(
        db, carrera_id, datos
    )

    if carrera is None:
        raise HTTPException(
            status_code=404,
            detail="Carrera no encontrada"
        )

    return carrera


@router.delete("/{carrera_id}", status_code=204)
def eliminar(
    carrera_id: int,
    db: Session = Depends(get_db)
):
    eliminado = carrera_service.eliminar_carrera(
        db, carrera_id
    )

    if not eliminado:
        raise HTTPException(
            status_code=404,
            detail="Carrera no encontrada"
        )
