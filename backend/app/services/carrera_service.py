
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.carrera import Carrera
from app.schemas.carrera import CarreraCreate, CarreraUpdate


def guardar_cambios(db: Session):
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Conflicto de integridad en la base de datos"
        )


def crear_carrera(db: Session, datos: CarreraCreate):
    carrera = Carrera(
        nombre=datos.nombre,
        descripcion=datos.descripcion,
        estado=True
    )

    db.add(carrera)
    guardar_cambios(db)
    db.refresh(carrera)

    return carrera


def listar_carreras(db: Session):
    consulta = (
        select(Carrera)
        .where(Carrera.estado.is_(True))
        .order_by(Carrera.id_carrera)
    )
    return db.scalars(consulta).all()


def obtener_carrera(db: Session, carrera_id: int):
    carrera = db.get(Carrera, carrera_id)

    if carrera is None or carrera.estado is not True:
        return None

    return carrera


def actualizar_carrera(
    db: Session,
    carrera_id: int,
    datos: CarreraUpdate
):
    carrera = obtener_carrera(db, carrera_id)

    if carrera is None:
        return None

    carrera.nombre = datos.nombre
    carrera.descripcion = datos.descripcion

    guardar_cambios(db)
    db.refresh(carrera)

    return carrera


def eliminar_carrera(db: Session, carrera_id: int):
    carrera = obtener_carrera(db, carrera_id)

    if carrera is None:
        return False

    carrera.estado = False
    guardar_cambios(db)

    return True
