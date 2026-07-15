import app.database as database
from typing import Any
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from schemas import Categoria

app = FastAPI()
@app.get("/")
def read_root():
    return {"Hello": "World"}
@app.get("/categorias")
def get_categorias(db = Depends(database.get_db))-> list[Categoria]:
    categorias = []
    cursor = db.cursor()
    cursor.execute("SELECT * FROM categorias")
    resultados = cursor.fetchall()
    for fila in resultados:
        categorias.append(Categoria(id=fila["id"], nombre=fila["titulo"]))


    return categorias
