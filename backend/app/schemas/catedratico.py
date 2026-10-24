
from pydantic import BaseModel, ConfigDict, Field, model_validator


class CatedraticoBase(BaseModel):
    codigo: str = Field(min_length=1, max_length=20)
    nombres: str = Field(min_length=1, max_length=100)
    apellidos: str = Field(min_length=1, max_length=100)
    correo: str = Field(min_length=1, max_length=120)
    carga_minima: int = Field(default=0, ge=0)
    carga_maxima: int = Field(ge=0)

    @model_validator(mode="after")
    def validar_carga(self):
        if self.carga_maxima < self.carga_minima:
            raise ValueError(
                "La carga máxima no puede ser menor "
                "que la carga mínima"
            )
        return self


class CatedraticoCreate(CatedraticoBase):
    pass


class CatedraticoUpdate(CatedraticoBase):
    pass


class CatedraticoResponse(CatedraticoBase):
    id: int = Field(validation_alias="id_profesor")
    estado: bool

    model_config = ConfigDict(from_attributes=True)

