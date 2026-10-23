
from pydantic import BaseModel, ConfigDict, Field


class AulaBase(BaseModel):
    codigo: str = Field(min_length=1, max_length=20)
    nombre: str = Field(min_length=1, max_length=80)
    capacidad: int = Field(gt=0)
    ubicacion: str | None = Field(default=None, max_length=100)
    estado: bool = True


class AulaCreate(AulaBase):
    pass


class AulaUpdate(BaseModel):
    codigo: str | None = Field(default=None, min_length=1, max_length=20)
    nombre: str | None = Field(default=None, min_length=1, max_length=80)
    capacidad: int | None = Field(default=None, gt=0)
    ubicacion: str | None = Field(default=None, max_length=100)
    estado: bool | None = None


class AulaResponse(AulaBase):
    id_aula: int

    model_config = ConfigDict(from_attributes=True)
