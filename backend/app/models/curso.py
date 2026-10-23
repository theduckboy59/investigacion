
from sqlalchemy import Boolean, ForeignKey, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Curso(Base):
    __tablename__ = "cursos"

    id_curso: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )

    codigo: Mapped[str | None] = mapped_column(
        String(20)
    )

    nombre: Mapped[str | None] = mapped_column(
        String(120)
    )

    horas_semanales: Mapped[int | None] = mapped_column(
        Integer
    )

    id_carrera: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("carreras.id_carrera")
    )

    id_ciclo: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("ciclos.id_ciclo")
    )

    estado: Mapped[bool | None] = mapped_column(
        Boolean, server_default=text("true")
    )
