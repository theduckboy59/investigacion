
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.periodo import PeriodoAcademico
from app.schemas.periodo import PeriodoCreate, PeriodoUpdate


def guardar_cambios(db: Session):
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Conflicto de integridad en la base de datos"
        )


def crear_periodo(db: Session, datos: PeriodoCreate):
    periodo = PeriodoAcademico(
        nombre=datos.nombre,
        fecha_inicio=datos.fecha_inicio,
        fecha_fin=datos.fecha_fin,
        estado=True
    )

    db.add(periodo)
    guardar_cambios(db)
    db.refresh(periodo)

    return periodo


def listar_periodos(db: Session):
    consulta = (
        select(PeriodoAcademico)
        .where(PeriodoAcademico.estado.is_(True))
        .order_by(PeriodoAcademico.id_periodo)
    )
    return db.scalars(consulta).all()


def obtener_periodo(db: Session, periodo_id: int):
    periodo = db.get(PeriodoAcademico, periodo_id)

    if periodo is None or periodo.estado is not True:
        return None

    return periodo


def actualizar_periodo(
    db: Session,
    periodo_id: int,
    datos: PeriodoUpdate
):
    periodo = obtener_periodo(db, periodo_id)

    if periodo is None:
        return None

    periodo.nombre = datos.nombre
    periodo.fecha_inicio = datos.fecha_inicio
    periodo.fecha_fin = datos.fecha_fin

    guardar_cambios(db)
    db.refresh(periodo)

    return periodo


def eliminar_periodo(db: Session, periodo_id: int):
    periodo = obtener_periodo(db, periodo_id)

    if periodo is None:
        return False

    periodo.estado = False
    guardar_cambios(db)

    return True
