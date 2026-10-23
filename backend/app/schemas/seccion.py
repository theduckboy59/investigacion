
from pydantic import BaseModel, ConfigDict, Field


class SeccionBase(BaseModel):
    codigo: str = Field(min_length=1, max_length=20)
    curso_id: int = Field(gt=0)
    periodo_id: int = Field(gt=0)
    alumnos_inscritos: int = Field(ge=0)


class SeccionCreate(SeccionBase):
    pass


class SeccionUpdate(SeccionBase):
    pass


class SeccionResponse(SeccionBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
