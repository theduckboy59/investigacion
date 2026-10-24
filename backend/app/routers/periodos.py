
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.periodo import (
    PeriodoCreate,
    PeriodoUpdate,
    PeriodoResponse,
)
from app.services import periodo_service


router = APIRouter(
    prefix="/api/periodos",
    tags=["Períodos académicos"]
)


@router.get("", response_model=list[PeriodoResponse])
def listar(db: Session = Depends(get_db)):
    return periodo_service.listar_periodos(db)


@router.get("/{periodo_id}", response_model=PeriodoResponse)
def obtener(
    periodo_id: int,
    db: Session = Depends(get_db)
):
    periodo = periodo_service.obtener_periodo(
        db, periodo_id
    )

    if periodo is None:
        raise HTTPException(
            status_code=404,
            detail="Período académico no encontrado"
        )

    return periodo


@router.post(
    "",
    response_model=PeriodoResponse,
    status_code=201
)
def crear(
    datos: PeriodoCreate,
    db: Session = Depends(get_db)
):
    return periodo_service.crear_periodo(db, datos)


@router.put(
    "/{periodo_id}",
    response_model=PeriodoResponse
)
def actualizar(
    periodo_id: int,
    datos: PeriodoUpdate,
    db: Session = Depends(get_db)
):
    periodo = periodo_service.actualizar_periodo(
        db, periodo_id, datos
    )

    if periodo is None:
        raise HTTPException(
            status_code=404,
            detail="Período académico no encontrado"
        )

    return periodo


@router.delete("/{periodo_id}", status_code=204)
def eliminar(
    periodo_id: int,
    db: Session = Depends(get_db)
):
    eliminado = periodo_service.eliminar_periodo(
        db, periodo_id
    )

    if not eliminado:
        raise HTTPException(
            status_code=404,
            detail="Período académico no encontrado"
        )
