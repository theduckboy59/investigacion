
from pydantic import BaseModel, ConfigDict, Field


class CicloBase(BaseModel):
    nombre: str = Field(min_length=1, max_length=50)
    orden: int = Field(ge=1)


class CicloCreate(CicloBase):
    pass


class CicloUpdate(CicloBase):
    pass


class CicloResponse(CicloBase):
    id: int = Field(validation_alias="id_ciclo")

    model_config = ConfigDict(from_attributes=True)

