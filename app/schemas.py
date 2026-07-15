from pydantic import BaseModel
from datetime import datetime as date

class Categoria(BaseModel):
    id: int
    nombre: str

class Plantilla(BaseModel):
    id: int
    nombre: str
    campos: str
    category_id: int
    es_default: int

class Tarea(BaseModel):
    id: int
    nombre: str
    campos: str | None
    fecha: date | None
    estado: str
    category_id: int | None
    template_id: int | None
