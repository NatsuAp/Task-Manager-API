from pydantic import BaseModel
from datetime import datetime as date

class Categoria(BaseModel):
    id: int
    nombre: str

class CrearCategoria(BaseModel):
    nombre: str

class Plantilla(BaseModel):
    id: int
    nombre: str
    campos: str
    category_id: int
    es_default: int

class CrearTarea(BaseModel):
    nombre: str
    descripcion: str | None
    fecha: str | None
    category_id: int

class Tarea(BaseModel):
    id: int
    nombre: str
    descripcion: str | None
    fecha: str | None
    estado: str | None
    category_id: int
