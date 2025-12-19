from pydantic import BaseModel, Field

class Ciudad(BaseModel):
    nombre: str = Field(..., min_length=2)
    latitud: float
    longitud: float
    temperatura: float
    clima: str