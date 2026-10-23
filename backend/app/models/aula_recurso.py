
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class AulaRecurso(Base):
    __tablename__ = "aula_recurso"

    id_aula: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("aulas.id_aula"),
        primary_key=True,
    )

    id_recurso: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("recursos.id_recurso"),
        primary_key=True,
    )

    cantidad: Mapped[int | None] = mapped_column(
        Integer,
        default=1,
        nullable=True,
    )
