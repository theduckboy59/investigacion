
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Ciclo(Base):
    __tablename__ = "ciclos"

    id_ciclo: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    nombre: Mapped[str | None] = mapped_column(
        String(50)
    )

    orden: Mapped[int | None] = mapped_column(
        Integer
    )
