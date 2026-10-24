
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.profesor_curso import (
    ProfesorCursoCreate,
    ProfesorCursoResponse,
)
from app.services import profesor_curso_service


router = APIRouter(
    prefix="/api/catedraticos",
    tags=["Profesor-Curso"]
)


@router.get(
    "/{id_profesor}/cursos",
    response_model=list[ProfesorCursoResponse]
)
def listar(
    id_profesor: int,
    db: Session = Depends(get_db)
):
    return profesor_curso_service.listar_cursos_profesor(
        db, id_profesor
    )


@router.post(
    "/{id_profesor}/cursos",
    response_model=ProfesorCursoResponse,
    status_code=201
)
def asignar(
    id_profesor: int,
    datos: ProfesorCursoCreate,
    db: Session = Depends(get_db)
):
    if datos.id_profesor != id_profesor:
        raise HTTPException(
            status_code=400,
            detail="El profesor de la ruta no coincide"
        )

    return profesor_curso_service.asignar_curso(db, datos)


@router.delete(
    "/{id_profesor}/cursos/{id_curso}",
    status_code=204
)
def quitar(
    id_profesor: int,
    id_curso: int,
    db: Session = Depends(get_db)
):
    eliminado = profesor_curso_service.quitar_curso(
        db, id_profesor, id_curso
    )

    if not eliminado:
        raise HTTPException(
            status_code=404,
            detail="Relación profesor-curso no encontrada"
        )
