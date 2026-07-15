import app.database as database
from typing import Any
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from app.schemas import Categoria
from app.routers.tareas import router as tareas_router
from app.routers.categorias import router as categorias_router
app = FastAPI()
app.include_router(tareas_router)

app.include_router(categorias_router)
@app.get("/")
def read_root():
    return {"Working :)"}

