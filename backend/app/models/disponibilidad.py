
from sqlalchemy import Boolean, ForeignKey, Integer, text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class DisponibilidadDocente(Base):
    __tablename__ = "disponibilidad_docente"

    id_profesor: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("profesores.id_profesor"),
        primary_key=True
    )

    id_bloque: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("bloques_horarios.id_bloque"),
        primary_key=True
    )

    disponible: Mapped[bool | None] = mapped_column(
        Boolean,
        server_default=text("true")
    )
