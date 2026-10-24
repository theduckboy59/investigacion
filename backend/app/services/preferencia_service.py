
from fastapi import HTTPException
from sqlalchemy import delete, select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.catedratico import Catedratico
from app.models.preferencia import PreferenciaDocente
from app.schemas.preferencia import PreferenciaUpdate


def validar_profesor(db: Session, id_profesor: int):
    profesor = db.get(Catedratico, id_profesor)

    if profesor is None or profesor.estado is not True:
        raise HTTPException(
            status_code=404,
            detail="Catedrático no encontrado o inactivo"
        )


def obtener_preferencias(db: Session, id_profesor: int):
    validar_profesor(db, id_profesor)

    consulta = (
        select(PreferenciaDocente)
        .where(PreferenciaDocente.id_profesor == id_profesor)
        .order_by(PreferenciaDocente.id_bloque)
    )

    return db.scalars(consulta).all()


def actualizar_preferencias(
    db: Session,
    id_profesor: int,
    datos: PreferenciaUpdate
):
    validar_profesor(db, id_profesor)

    ids = [p.id_bloque for p in datos.preferencias]

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
            delete(PreferenciaDocente).where(
                PreferenciaDocente.id_profesor == id_profesor
            )
        )

        for preferencia in datos.preferencias:
            db.add(
                PreferenciaDocente(
                    id_profesor=id_profesor,
                    id_bloque=preferencia.id_bloque,
                    valor_preferencia=preferencia.valor_preferencia,
                    observacion=preferencia.observacion
                )
            )

        db.commit()

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Conflicto al guardar preferencias"
        )

    return obtener_preferencias(db, id_profesor)
