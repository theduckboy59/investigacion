
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.seccion import (
    SeccionCreate,
    SeccionUpdate,
    SeccionResponse,
)
from app.services import seccion_service


router = APIRouter(
    prefix="/api/secciones",
    tags=["Secciones"]
)


@router.get("", response_model=list[SeccionResponse])
def listar(db: Session = Depends(get_db)):
    return seccion_service.listar_secciones(db)


@router.get("/{seccion_id}", response_model=SeccionResponse)
def obtener(
    seccion_id: int,
    db: Session = Depends(get_db)
):
    seccion = seccion_service.obtener_seccion(
        db, seccion_id
    )

    if seccion is None:
        raise HTTPException(
            status_code=404,
            detail="Sección no encontrada"
        )

    return seccion


@router.post(
    "",
    response_model=SeccionResponse,
    status_code=201
)
def crear(
    datos: SeccionCreate,
    db: Session = Depends(get_db)
):
    return seccion_service.crear_seccion(db, datos)


@router.put(
    "/{seccion_id}",
    response_model=SeccionResponse
)
def actualizar(
    seccion_id: int,
    datos: SeccionUpdate,
    db: Session = Depends(get_db)
):
    seccion = seccion_service.actualizar_seccion(
        db, seccion_id, datos
    )

    if seccion is None:
        raise HTTPException(
            status_code=404,
            detail="Sección no encontrada"
        )

    return seccion


@router.delete("/{seccion_id}", status_code=204)
def eliminar(
    seccion_id: int,
    db: Session = Depends(get_db)
):
    eliminado = seccion_service.eliminar_seccion(
        db, seccion_id
    )

    if not eliminado:
        raise HTTPException(
            status_code=404,
            detail="Sección no encontrada"
        )
