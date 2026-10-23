
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.curso import Curso
from app.schemas.curso import CursoCreate, CursoUpdate


def crear_curso(db: Session, datos: CursoCreate):
    curso = Curso(
        codigo=datos.codigo,
        nombre=datos.nombre,
        horas_semanales=datos.periodos_por_semana,
        id_carrera=datos.id_carrera,
        id_ciclo=datos.id_ciclo,
    )

    db.add(curso)
    db.commit()
    db.refresh(curso)

    return curso


def listar_cursos(db: Session):
    consulta = select(Curso).order_by(Curso.id_curso)
    return db.scalars(consulta).all()


def obtener_curso(db: Session, curso_id: int):
    return db.get(Curso, curso_id)


def actualizar_curso(
    db: Session,
    curso_id: int,
    datos: CursoUpdate,
):
    curso = db.get(Curso, curso_id)

    if curso is None:
        return None

    curso.codigo = datos.codigo
    curso.nombre = datos.nombre
    curso.horas_semanales = datos.periodos_por_semana
    curso.id_carrera = datos.id_carrera
    curso.id_ciclo = datos.id_ciclo

    db.commit()
    db.refresh(curso)

    return curso


def eliminar_curso(db: Session, curso_id: int):
    curso = db.get(Curso, curso_id)

    if curso is None:
        return False

    db.delete(curso)
    db.commit()

    return True
