
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.ciclo import Ciclo
from app.schemas.ciclo import CicloCreate, CicloUpdate


def guardar_cambios(db: Session):
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Conflicto de integridad en la base de datos"
        )


def crear_ciclo(db: Session, datos: CicloCreate):
    ciclo = Ciclo(
        nombre=datos.nombre,
        orden=datos.orden
    )

    db.add(ciclo)
    guardar_cambios(db)
    db.refresh(ciclo)

    return ciclo


def listar_ciclos(db: Session):
    consulta = select(Ciclo).order_by(Ciclo.id_ciclo)
    return db.scalars(consulta).all()


def obtener_ciclo(db: Session, ciclo_id: int):
    return db.get(Ciclo, ciclo_id)


def actualizar_ciclo(
    db: Session,
    ciclo_id: int,
    datos: CicloUpdate
):
    ciclo = obtener_ciclo(db, ciclo_id)

    if ciclo is None:
        return None

    ciclo.nombre = datos.nombre
    ciclo.orden = datos.orden

    guardar_cambios(db)
    db.refresh(ciclo)

    return ciclo


def eliminar_ciclo(db: Session, ciclo_id: int):
    ciclo = obtener_ciclo(db, ciclo_id)

    if ciclo is None:
        return False

    try:
        db.delete(ciclo)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="No se puede eliminar un ciclo relacionado"
        )

    return True
¿
