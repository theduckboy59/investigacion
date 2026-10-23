
from pydantic import BaseModel, ConfigDict, Field


class CursoBase(BaseModel):
    codigo: str = Field(min_length=1, max_length=20)
    nombre: str = Field(min_length=1, max_length=120)
    periodos_por_semana: int = Field(gt=0)
    id_carrera: int = Field(gt=0)
    id_ciclo: int = Field(gt=0)


class CursoCreate(CursoBase):
    pass


class CursoUpdate(CursoBase):
    pass



class CursoResponse(CursoBase):
    id: int = Field(validation_alias="id_curso")

    periodos_por_semana: int = Field(
        gt=0,
        validation_alias="horas_semanales"
    )

    model_config = ConfigDict(from_attributes=True)


