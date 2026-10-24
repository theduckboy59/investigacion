
from pydantic import BaseModel, ConfigDict, Field


class CarreraBase(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)
    descripcion: str | None = None


class CarreraCreate(CarreraBase):
    pass


class CarreraUpdate(CarreraBase):
    pass


class CarreraResponse(CarreraBase):
    id: int = Field(validation_alias="id_carrera")
    estado: bool

    model_config = ConfigDict(from_attributes=True)

