from pydantic import BaseModel, json


class CrearPlantilla(BaseModel):
    nombre: str
    category_id: int
    campos: str


class Plantilla(BaseModel):
    id: int
    nombre: str
    category_id: int
    campos : str
    es_default: bool

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

class ActualizarCategoria(BaseModel):
    titulo: str

class CrearTarea(BaseModel):
    nombre: str
    descripcion: str | None = None
    fecha: str | None = None
    category_id: int

class ActualizarTarea(BaseModel):
    titulo: str | None = None
    descripcion: str | None = None
    fecha: str | None = None
    estado: str | None = None
    category_id: int | None = None

class Tarea(BaseModel):
    id: int
    nombre: str
    descripcion: str | None = None
    fecha: str | None = None
    estado: str | None = None
    category_id: int
