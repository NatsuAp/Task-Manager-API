
from app.schemas import CrearTarea
from app.schemas import Tarea
import app.database as database
from fastapi import FastAPI, Depends, APIRouter

router = APIRouter()
@router.post("/tareas")
def crear_tarea(tarea: CrearTarea, db = Depends(database.get_db)) -> Tarea:

    cursor = db.cursor()
    estado = 'Pendiente'
    print(tarea)
    cursor.execute('PRAGMA foreign_keys = ON;')
    cursor.execute("insert into tareas (titulo, descripcion, fecha, estado, category_id) values (?, ?, ?, ?, ?)", (tarea.nombre, tarea.descripcion, tarea.fecha, estado, tarea.category_id))
    db.commit()
    tarea_id = cursor.lastrowid


    return Tarea(id=tarea_id,
                 nombre=tarea.nombre,
                 descripcion=tarea.descripcion,
                 fecha=tarea.fecha,
                 estado="Pendiente",
                 category_id=tarea.category_id)


#
# class CrearTarea(BaseModel):
#     nombre: str
#     descripcion: str | None
#     fecha: str | None
#     category_id: int
# class Tarea(BaseModel):
#     id: int
#     nombre: str
#     descripcion: str | None
#     fecha: str | None
#     estado: str | None
#     category_id: int