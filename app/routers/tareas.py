from fastapi import HTTPException
from typing import Tuple

from starlette import status

from app.schemas import CrearTarea
from app.schemas import Tarea
import app.database as database
from fastapi import FastAPI, Depends, APIRouter

router = APIRouter()
@router.post("/tareas")
def crear_tarea(tarea: CrearTarea, db = Depends(database.get_db)) -> Tarea:

    cursor = db.cursor()
    estado = 'Pendiente'


    cursor.execute("insert into tareas (titulo, descripcion, fecha, estado, category_id) values (?, ?, ?, ?, ?)", (tarea.nombre, tarea.descripcion, tarea.fecha, estado, tarea.category_id))
    db.commit()
    tarea_id = cursor.lastrowid


    return Tarea(id=tarea_id,
                 nombre=tarea.nombre,
                 descripcion=tarea.descripcion,
                 fecha=tarea.fecha,
                 estado= estado,
                 category_id=tarea.category_id)

@router.get("/tareas")
def get_tareas(category_id: int | None = None, db = Depends(database.get_db))-> list[Tarea]:
    cursor = db.cursor()
    query = "SELECT * FROM tareas "

    params = ()
    if category_id is not None:
        query += f"WHERE category_id = ?"
        params = (category_id,)
    cursor.execute(query, params)


    resultados = cursor.fetchall()
    tareas = []
    for tarea in resultados:
        #cursor.execute("SELECT titulo FROM categorias  WHERE id = ?", (category_id,))
        tareas.append(Tarea(id=tarea["id"],nombre=tarea["titulo"],descripcion=tarea["descripcion"],fecha=tarea["fecha"],estado=tarea["estado"], category_id=tarea["category_id"]))

    return tareas

@router.get("/tareas/{id}")
def get_tarea(id: int, db = Depends(database.get_db)) -> Tarea:
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tareas WHERE id = ?", (id,))
    resultado = cursor.fetchone()
    if resultado == None :
        raise HTTPException(status_code=404, detail=" Tarea no encontrada")

    return Tarea(id=resultado["id"],
                 nombre=resultado["titulo"],
                 descripcion=resultado["descripcion"],
                 fecha=resultado["fecha"],
                 estado=resultado["estado"],
                 category_id=resultado["category_id"])



