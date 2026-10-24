
from datetime import date

from sqlalchemy import Boolean, Date, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class PeriodoAcademico(Base):
    __tablename__ = "periodos_academicos"

    id_periodo: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    nombre: Mapped[str | None] = mapped_column(
        String(30)
    )

    fecha_inicio: Mapped[date | None] = mapped_column(
        Date
    )

    fecha_fin: Mapped[date | None] = mapped_column(
        Date
    )

    estado: Mapped[bool | None] = mapped_column(
        Boolean,
        server_default=text("true")
    )
