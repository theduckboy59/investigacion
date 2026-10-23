
from pydantic import BaseModel, ConfigDict, Field


class ProfesorCursoBase(BaseModel):
    id_profesor: int = Field(gt=0)
    id_curso: int = Field(gt=0)


class ProfesorCursoCreate(ProfesorCursoBase):
    pass


class ProfesorCursoResponse(ProfesorCursoBase):
    model_config = ConfigDict(from_attributes=True)
