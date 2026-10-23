
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.curso import (
    CursoCreate,
    CursoUpdate,
    CursoResponse,
)
from app.services import curso_service

router = APIRouter(
    prefix="/api/cursos",
    tags=["Cursos"]
)


@router.get("", response_model=list[CursoResponse])
def listar(db: Session = Depends(get_db)):
    return curso_service.listar_cursos(db)


@router.get("/{curso_id}", response_model=CursoResponse)
def obtener(curso_id: int, db: Session = Depends(get_db)):
    curso = curso_service.obtener_curso(db, curso_id)
    if curso is None:
        raise HTTPException(404, "Curso no encontrado")
    return curso


@router.post("", response_model=CursoResponse, status_code=201)
def crear(datos: CursoCreate, db: Session = Depends(get_db)):
    return curso_service.crear_curso(db, datos)


@router.put("/{curso_id}", response_model=CursoResponse)
def actualizar(
    curso_id: int,
    datos: CursoUpdate,
    db: Session = Depends(get_db),
):
    curso = curso_service.actualizar_curso(
        db, curso_id, datos
    )
    if curso is None:
        raise HTTPException(404, "Curso no encontrado")
    return curso


@router.delete("/{curso_id}", status_code=204)
def eliminar(curso_id: int, db: Session = Depends(get_db)):
    eliminado = curso_service.eliminar_curso(db, curso_id)
    if not eliminado:
        raise HTTPException(404, "Curso no encontrado")
