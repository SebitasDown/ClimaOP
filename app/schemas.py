from pydantic import BaseModel, Field

class Ciudad(BaseModel):
    nombre: str = Field(..., min_length=2)
    latitud: float | None = None
    longitud: float | None = None
    temperatura: float | None = None
    clima: str | None = None