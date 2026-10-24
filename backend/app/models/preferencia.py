
from sqlalchemy import ForeignKey, Integer, SmallInteger, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class PreferenciaDocente(Base):
    __tablename__ = "preferencias_docente"

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

    valor_preferencia: Mapped[int | None] = mapped_column(
        SmallInteger
    )

    observacion: Mapped[str | None] = mapped_column(
        Text
    )
