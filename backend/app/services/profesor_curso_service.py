
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.catedratico import Catedratico
from app.models.curso import Curso
from app.models.profesor_curso import ProfesorCurso
from app.schemas.profesor_curso import ProfesorCursoCreate


def validar_relaciones(db: Session, datos: ProfesorCursoCreate):
    profesor = db.get(Catedratico, datos.id_profesor)

    if profesor is None or profesor.estado is not True:
        raise HTTPException(
            status_code=404,
            detail="El catedrático no existe o está inactivo"
        )

    curso = db.get(Curso, datos.id_curso)

    if curso is None or curso.estado is not True:
        raise HTTPException(
            status_code=404,
            detail="El curso no existe o está inactivo"
        )


def listar_cursos_profesor(db: Session, id_profesor: int):
    profesor = db.get(Catedratico, id_profesor)

    if profesor is None or profesor.estado is not True:
        raise HTTPException(
            status_code=404,
            detail="Catedrático no encontrado"
        )

    consulta = (
        select(ProfesorCurso)
        .join(Curso, ProfesorCurso.id_curso == Curso.id_curso)
        .where(
            ProfesorCurso.id_profesor == id_profesor,
            Curso.estado.is_(True)
        )
        .order_by(ProfesorCurso.id_curso)
    )

    return db.scalars(consulta).all()


def asignar_curso(db: Session, datos: ProfesorCursoCreate):
    validar_relaciones(db, datos)

    existente = db.get(
        ProfesorCurso,
        (datos.id_profesor, datos.id_curso)
    )

    if existente is not None:
        raise HTTPException(
            status_code=409,
            detail="El profesor ya tiene asignado este curso"
        )

    relacion = ProfesorCurso(
        id_profesor=datos.id_profesor,
        id_curso=datos.id_curso
    )

    try:
        db.add(relacion)
        db.commit()
        db.refresh(relacion)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Conflicto al asignar el curso"
        )

    return relacion


def quitar_curso(
    db: Session,
    id_profesor: int,
    id_curso: int
):
    relacion = db.get(
        ProfesorCurso,
        (id_profesor, id_curso)
    )

    if relacion is None:
        return False

    try:
        db.delete(relacion)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="No se pudo quitar la relación"
        )

    return True
