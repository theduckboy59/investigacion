
from fastapi import HTTPException
from sqlalchemy import delete, select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.catedratico import Catedratico
from app.models.disponibilidad import DisponibilidadDocente
from app.schemas.disponibilidad import DisponibilidadUpdate


def validar_profesor(db: Session, id_profesor: int):
    profesor = db.get(Catedratico, id_profesor)

    if profesor is None or profesor.estado is not True:
        raise HTTPException(
            status_code=404,
            detail="Catedrático no encontrado o inactivo"
        )


def obtener_disponibilidad(db: Session, id_profesor: int):
    validar_profesor(db, id_profesor)

    consulta = (
        select(DisponibilidadDocente)
        .where(
            DisponibilidadDocente.id_profesor == id_profesor
        )
        .order_by(DisponibilidadDocente.id_bloque)
    )

    return db.scalars(consulta).all()


def actualizar_disponibilidad(
    db: Session,
    id_profesor: int,
    datos: DisponibilidadUpdate
):
    validar_profesor(db, id_profesor)

    ids = [bloque.id_bloque for bloque in datos.bloques]

    if len(ids) != len(set(ids)):
        raise HTTPException(
            status_code=400,
            detail="No se permiten bloques repetidos"
        )

    if ids:
        existentes = db.execute(
            text(
                "SELECT id_bloque FROM bloques_horarios "
                "WHERE id_bloque = ANY(:ids) "
                "AND estado = TRUE"
            ),
            {"ids": ids}
        ).scalars().all()

        if set(ids) != set(existentes):
            raise HTTPException(
                status_code=400,
                detail="Hay bloques inexistentes o inactivos"
            )

    try:
        db.execute(
            delete(DisponibilidadDocente).where(
                DisponibilidadDocente.id_profesor == id_profesor
            )
        )

        for bloque in datos.bloques:
            db.add(
                DisponibilidadDocente(
                    id_profesor=id_profesor,
                    id_bloque=bloque.id_bloque,
                    disponible=bloque.disponible
                )
            )

        db.commit()

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Conflicto al guardar disponibilidad"
        )

    return obtener_disponibilidad(db, id_profesor)
