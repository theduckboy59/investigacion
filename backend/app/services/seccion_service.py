
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.seccion import Seccion
from app.models.curso import Curso
from app.models.periodo import PeriodoAcademico
from app.schemas.seccion import SeccionCreate, SeccionUpdate


def validar_relaciones(db: Session, datos):
    curso = db.get(Curso, datos.curso_id)

    if curso is None or curso.estado is not True:
        raise HTTPException(
            status_code=400,
            detail="El curso no existe o está inactivo"
        )

    periodo = db.get(PeriodoAcademico, datos.periodo_id)

    if periodo is None or periodo.estado is not True:
        raise HTTPException(
            status_code=400,
            detail="El período no existe o está inactivo"
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


def crear_seccion(db: Session, datos: SeccionCreate):
    validar_relaciones(db, datos)

    seccion = Seccion(
        codigo=datos.codigo,
        id_curso=datos.curso_id,
        id_periodo=datos.periodo_id,
        cantidad_estudiantes=datos.alumnos_inscritos,
        estado=True
    )

    db.add(seccion)
    guardar_cambios(db)
    db.refresh(seccion)

    return seccion


def listar_secciones(db: Session):
    consulta = (
        select(Seccion)
        .where(Seccion.estado.is_(True))
        .order_by(Seccion.id_seccion)
    )
    return db.scalars(consulta).all()


def obtener_seccion(db: Session, seccion_id: int):
    seccion = db.get(Seccion, seccion_id)

    if seccion is None or seccion.estado is not True:
        return None

    return seccion


def actualizar_seccion(
    db: Session,
    seccion_id: int,
    datos: SeccionUpdate
):
    seccion = obtener_seccion(db, seccion_id)

    if seccion is None:
        return None

    validar_relaciones(db, datos)

    seccion.codigo = datos.codigo
    seccion.id_curso = datos.curso_id
    seccion.id_periodo = datos.periodo_id
    seccion.cantidad_estudiantes = datos.alumnos_inscritos

    guardar_cambios(db)
    db.refresh(seccion)

    return seccion


def eliminar_seccion(db: Session, seccion_id: int):
    seccion = obtener_seccion(db, seccion_id)

    if seccion is None:
        return False

    seccion.estado = False
    guardar_cambios(db)

    return True
