
from pydantic import BaseModel, ConfigDict, Field


class CatedraticoBase(BaseModel):
    codigo: str = Field(min_length=1, max_length=20)
    nombres: str = Field(min_length=1, max_length=100)
    apellidos: str = Field(min_length=1, max_length=100)
    correo: str = Field(min_length=1, max_length=120)
    carga_minima: int = Field(default=0, ge=0)
    carga_maxima: int = Field(ge=0)


class CatedraticoCreate(CatedraticoBase):
    pass


class CatedraticoUpdate(CatedraticoBase):
    pass


class CatedraticoResponse(CatedraticoBase):
    id: int
    estado: bool

    model_config = ConfigDict(from_attributes=True)
