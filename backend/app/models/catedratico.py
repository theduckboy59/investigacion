
from sqlalchemy import Boolean, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Catedratico(Base):
    __tablename__ = "profesores"

    id_profesor: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )

    codigo: Mapped[str | None] = mapped_column(
        String(20)
    )

    nombres: Mapped[str | None] = mapped_column(
        String(100)
    )

    apellidos: Mapped[str | None] = mapped_column(
        String(100)
    )

    correo: Mapped[str | None] = mapped_column(
        String(120)
    )

    carga_minima: Mapped[int | None] = mapped_column(
        Integer, server_default=text("0")
    )

    carga_maxima: Mapped[int | None] = mapped_column(
        Integer
    )

    estado: Mapped[bool | None] = mapped_column(
        Boolean, server_default=text("true")
    )
