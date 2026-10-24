
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ProfesorCurso(Base):
    __tablename__ = "profesor_curso"

    id_profesor: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("profesores.id_profesor"),
        primary_key=True
    )

    id_curso: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("cursos.id_curso"),
        primary_key=True
    )
