
from pydantic import BaseModel, ConfigDict, Field


class DisponibilidadBase(BaseModel):
    id_bloque: int = Field(gt=0)
    disponible: bool = True


class DisponibilidadResponse(DisponibilidadBase):
    id_profesor: int = Field(gt=0)

    model_config = ConfigDict(from_attributes=True)


class DisponibilidadUpdate(BaseModel):
    bloques: list[DisponibilidadBase]
