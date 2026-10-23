
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.aula import Aula
from app.schemas.aula import AulaCreate, AulaResponse, AulaUpdate

router = APIRouter(prefix="/api/aulas", tags=["Aulas"])


@router.post(
    "",
    response_model=AulaResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear_aula(datos: AulaCreate, db: Session = Depends(get_db)):
    aula = Aula(**datos.model_dump())
    db.add(aula)
    db.commit()
    db.refresh(aula)
    return aula


@router.get("", response_model=list[AulaResponse])
def listar_aulas(db: Session = Depends(get_db)):
    return db.query(Aula).order_by(Aula.id_aula).all()


@router.get("/{id_aula}", response_model=AulaResponse)
def consultar_aula(id_aula: int, db: Session = Depends(get_db)):
    aula = db.get(Aula, id_aula)

    if aula is None:
        raise HTTPException(status_code=404, detail="Aula no encontrada")

    return aula


@router.put("/{id_aula}", response_model=AulaResponse)
def actualizar_aula(
    id_aula: int,
    datos: AulaUpdate,
    db: Session = Depends(get_db),
):
    aula = db.get(Aula, id_aula)

    if aula is None:
        raise HTTPException(status_code=404, detail="Aula no encontrada")

    cambios = datos.model_dump(exclude_unset=True)

    for campo, valor in cambios.items():
        setattr(aula, campo, valor)

    db.commit()
    db.refresh(aula)
    return aula


@router.delete("/{id_aula}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_aula(id_aula: int, db: Session = Depends(get_db)):
    aula = db.get(Aula, id_aula)

    if aula is None:
        raise HTTPException(status_code=404, detail="Aula no encontrada")

    # Desactivación lógica: conserva el registro en PostgreSQL.
    aula.estado = False
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
