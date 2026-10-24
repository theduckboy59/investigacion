
from pydantic import BaseModel, ConfigDict, Field


class PreferenciaBase(BaseModel):
    id_bloque: int = Field(gt=0)
    valor_preferencia: int = Field(ge=1, le=5)
    observacion: str | None = None


class PreferenciaResponse(PreferenciaBase):
    id_profesor: int = Field(gt=0)

    model_config = ConfigDict(from_attributes=True)


class PreferenciaUpdate(BaseModel):
    preferencias: list[PreferenciaBase]
