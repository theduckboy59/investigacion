
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.curso import Curso
from app.models.carrera import Carrera
from app.models.ciclo import Ciclo
from app.schemas.curso import CursoCreate, CursoUpdate


def validar_relaciones(db: Session, datos):
    carrera = db.get(Carrera, datos.id_carrera)

    if carrera is None or carrera.estado is not True:
        raise HTTPException(
            status_code=400,
            detail="La carrera no existe o está inactiva"
        )

    ciclo = db.get(Ciclo, datos.id_ciclo)

    if ciclo is None:
        raise HTTPException(
            status_code=400,
            detail="El ciclo académico no existe"
        )


def guardar_cambios(db: Session):
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Conflicto de integridad en la base de datos"
        )


def crear_curso(db: Session, datos: CursoCreate):
    validar_relaciones(db, datos)

    curso = Curso(
        codigo=datos.codigo,
        nombre=datos.nombre,
        horas_semanales=datos.periodos_por_semana,
        id_carrera=datos.id_carrera,
        id_ciclo=datos.id_ciclo,
        estado=True
    )

    db.add(curso)
    guardar_cambios(db)
    db.refresh(curso)

    return curso


def listar_cursos(db: Session):
    consulta = (
        select(Curso)
        .where(Curso.estado.is_(True))
        .order_by(Curso.id_curso)
    )

    return db.scalars(consulta).all()


def obtener_curso(db: Session, curso_id: int):
    curso = db.get(Curso, curso_id)

    if curso is None or curso.estado is not True:
        return None

    return curso


def actualizar_curso(
    db: Session,
    curso_id: int,
    datos: CursoUpdate
):
    curso = obtener_curso(db, curso_id)

    if curso is None:
        return None

    validar_relaciones(db, datos)

    curso.codigo = datos.codigo
    curso.nombre = datos.nombre
    curso.horas_semanales = datos.periodos_por_semana
    curso.id_carrera = datos.id_carrera
    curso.id_ciclo = datos.id_ciclo

    guardar_cambios(db)
    db.refresh(curso)

    return curso


def eliminar_curso(db: Session, curso_id: int):
    curso = obtener_curso(db, curso_id)

    if curso is None:
        return False

    curso.estado = False
    guardar_cambios(db)

    return True

