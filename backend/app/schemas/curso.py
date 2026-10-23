
from pydantic import BaseModel, Field, ConfigDict


class CursoBase(BaseModel):
    codigo: str = Field(min_length=1, max_length=20)
    nombre: str = Field(min_length=1, max_length=120)
    periodos_por_semana: int = Field(gt=0)


class CursoCreate(CursoBase):
    pass


class CursoUpdate(CursoBase):
    pass


class CursoResponse(CursoBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
