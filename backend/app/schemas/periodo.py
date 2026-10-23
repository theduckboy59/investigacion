
from datetime import date

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    model_validator,
)


class PeriodoBase(BaseModel):
    nombre: str = Field(min_length=1, max_length=30)
    fecha_inicio: date
    fecha_fin: date

    @model_validator(mode="after")
    def validar_fechas(self):
        if self.fecha_fin < self.fecha_inicio:
            raise ValueError(
                "La fecha de fin no puede ser anterior "
                "a la fecha de inicio"
            )
        return self


class PeriodoCreate(PeriodoBase):
    pass


class PeriodoUpdate(PeriodoBase):
    pass


class PeriodoResponse(PeriodoBase):
    id: int
    estado: bool

    model_config = ConfigDict(from_attributes=True)
