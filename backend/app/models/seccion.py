
from sqlalchemy import Boolean, ForeignKey, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Seccion(Base):
    __tablename__ = "secciones"

    id_seccion: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )

    codigo: Mapped[str | None] = mapped_column(
        String(20)
    )

    id_curso: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("cursos.id_curso")
    )

    nombre: Mapped[str | None] = mapped_column(
        String(10)
    )

    cantidad_estudiantes: Mapped[int | None] = mapped_column(
        Integer
    )

    id_periodo: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("periodos_academicos.id_periodo")
    )

    estado: Mapped[bool | None] = mapped_column(
        Boolean, server_default=text("true")
    )
