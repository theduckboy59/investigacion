
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.catedratico import (
    CatedraticoCreate,
    CatedraticoUpdate,
    CatedraticoResponse,
)
from app.services import catedratico_service


router = APIRouter(
    prefix="/api/catedraticos",
    tags=["Catedráticos"]
)


@router.get("", response_model=list[CatedraticoResponse])
def listar(db: Session = Depends(get_db)):
    return catedratico_service.listar_catedraticos(db)


@router.get("/{catedratico_id}", response_model=CatedraticoResponse)
def obtener(
    catedratico_id: int,
    db: Session = Depends(get_db)
):
    catedratico = catedratico_service.obtener_catedratico(
        db, catedratico_id
    )

    if catedratico is None:
        raise HTTPException(
            status_code=404,
            detail="Catedrático no encontrado"
        )

    return catedratico


@router.post(
    "",
    response_model=CatedraticoResponse,
    status_code=201
)
def crear(
    datos: CatedraticoCreate,
    db: Session = Depends(get_db)
):
    return catedratico_service.crear_catedratico(db, datos)


@router.put(
    "/{catedratico_id}",
    response_model=CatedraticoResponse
)
def actualizar(
    catedratico_id: int,
    datos: CatedraticoUpdate,
    db: Session = Depends(get_db)
):
    catedratico = catedratico_service.actualizar_catedratico(
        db, catedratico_id, datos
    )

    if catedratico is None:
        raise HTTPException(
            status_code=404,
            detail="Catedrático no encontrado"
        )

    return catedratico


@router.delete("/{catedratico_id}", status_code=204)
def eliminar(
    catedratico_id: int,
    db: Session = Depends(get_db)
):
    eliminado = catedratico_service.eliminar_catedratico(
        db, catedratico_id
    )

    if not eliminado:
        raise HTTPException(
            status_code=404,
            detail="Catedrático no encontrado"
        )
