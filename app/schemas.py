from pydantic import BaseModel, json
from typing import Any
from psycopg2.extras import Json

class CrearPlantilla(BaseModel):
    titulo_plantilla: str
    category_id: int | None = None
    campos: dict[str, str]

class ActualizarPlantilla(BaseModel):
    titulo_plantilla: str | None = None
    category_id: int | None = None
    campos: dict[str, str] | None = None

class Plantilla(BaseModel):
    id: int
    titulo_plantilla: str
    category_id: int | None = None
    campos : dict[str, str]
    es_default: bool

class Categoria(BaseModel):
    id: int
    titulo_categoria: str

class CrearCategoria(BaseModel):
    titulo_categoria: str

class ActualizarCategoria(BaseModel):
    titulo_categoria: str

class CrearTarea(BaseModel):
    titulo_tarea: str
    descripcion: str | None = None
    fecha: str | None = None
    category_id: int
    template_id: int | None = None
    campos: dict[str, str] | None = None

class ActualizarTarea(BaseModel):
    titulo_tarea: str | None = None
    descripcion: str | None = None
    fecha: str | None = None
    estado: str | None = None
    category_id: int | None = None
    template_id: int | None = None
    campos: dict[str, str] | None = None

class Tarea(BaseModel):
    id: int
    titulo_tarea: str
    descripcion: str | None = None
    fecha: str | None = None
    estado: str | None = None
    category_id: int
    template_id: int | None = None
    campos: dict[str, str] | None = None
