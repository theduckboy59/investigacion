
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.catedratico import Catedratico
from app.schemas.catedratico import (
    CatedraticoCreate,
    CatedraticoUpdate,
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


def crear_catedratico(db: Session, datos: CatedraticoCreate):
    catedratico = Catedratico(
        codigo=datos.codigo,
        nombres=datos.nombres,
        apellidos=datos.apellidos,
        correo=datos.correo,
        carga_minima=datos.carga_minima,
        carga_maxima=datos.carga_maxima,
        estado=True
    )

    db.add(catedratico)
    guardar_cambios(db)
    db.refresh(catedratico)

    return catedratico


def listar_catedraticos(db: Session):
    consulta = (
        select(Catedratico)
        .where(Catedratico.estado.is_(True))
        .order_by(Catedratico.id_profesor)
    )
    return db.scalars(consulta).all()


def obtener_catedratico(db: Session, catedratico_id: int):
    catedratico = db.get(Catedratico, catedratico_id)

    if catedratico is None or catedratico.estado is not True:
        return None

    return catedratico


def actualizar_catedratico(
    db: Session,
    catedratico_id: int,
    datos: CatedraticoUpdate
):
    catedratico = obtener_catedratico(db, catedratico_id)

    if catedratico is None:
        return None

    catedratico.codigo = datos.codigo
    catedratico.nombres = datos.nombres
    catedratico.apellidos = datos.apellidos
    catedratico.correo = datos.correo
    catedratico.carga_minima = datos.carga_minima
    catedratico.carga_maxima = datos.carga_maxima

    guardar_cambios(db)
    db.refresh(catedratico)

    return catedratico


def eliminar_catedratico(db: Session, catedratico_id: int):
    catedratico = obtener_catedratico(db, catedratico_id)

    if catedratico is None:
        return False

    catedratico.estado = False
    guardar_cambios(db)

    return True
