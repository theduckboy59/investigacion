
from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

# Modelo que representa la tabla aulas de PostgreSQL.
# La clase Base se conectará con la configuración común del proyecto.
from app.database import Base


class Aula(Base):
    __tablename__ = "aulas"

    id_aula: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    codigo: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    nombre: Mapped[str | None] = mapped_column(
        String(80),
        nullable=True
    )

    capacidad: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    ubicacion: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    estado: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )
