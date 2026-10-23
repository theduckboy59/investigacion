
from sqlalchemy import Boolean, Integer, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Carrera(Base):
    __tablename__ = "carreras"

    id_carrera: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    nombre: Mapped[str | None] = mapped_column(
        String(100)
    )

    descripcion: Mapped[str | None] = mapped_column(
        Text
    )

    estado: Mapped[bool | None] = mapped_column(
        Boolean,
        server_default=text("true")
    )
