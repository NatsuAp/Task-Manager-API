from fastapi import HTTPException
from app.schemas import CrearTarea, Tarea, ActualizarTarea
import app.database as database
from fastapi import Depends, APIRouter
from pydantic import BaseModel
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
    if resultado is None:
        raise HTTPException(status_code=404, detail=" Tarea no encontrada")

    return Tarea(id=resultado["id"],
                 nombre=resultado["titulo"],
                 descripcion=resultado["descripcion"],
                 fecha=resultado["fecha"],
                 estado=resultado["estado"],
                 category_id=resultado["category_id"])



@router.patch("/tareas/{id}")
def actualizar_tarea(id: int, tarea_a_actualizar: ActualizarTarea, db = Depends(database.get_db)) -> Tarea:


    data = {
        "titulo": tarea_a_actualizar.titulo,
        "descripcion": tarea_a_actualizar.descripcion,
        "fecha": tarea_a_actualizar.fecha,
        "estado": tarea_a_actualizar.estado,
        "category_id": tarea_a_actualizar.category_id,
    }


    cursor = db.cursor()
    cursor.execute("SELECT * FROM tareas WHERE id = ?", (id,))
    resultado = cursor.fetchone()
    if resultado is None:
        raise HTTPException(status_code=404, detail=" Tarea no encontrada")
    tarea_final = Tarea(id=resultado["id"],
                 nombre=resultado["titulo"],
                 descripcion=resultado["descripcion"],
                 fecha=resultado["fecha"],
                 estado=resultado["estado"],
                 category_id=resultado["category_id"]
                 )

    if tarea_a_actualizar.titulo is not None:
        tarea_final.nombre = tarea_a_actualizar.titulo
    if tarea_a_actualizar.descripcion is not None:
        tarea_final.descripcion = tarea_a_actualizar.descripcion
    if tarea_a_actualizar.fecha is not None:
        tarea_final.fecha = tarea_a_actualizar.fecha
    if tarea_a_actualizar.estado is not None:
        tarea_final.estado = tarea_a_actualizar.estado
    if tarea_a_actualizar.category_id is not None:
        tarea_final.category_id = tarea_a_actualizar.category_id


    datos = tarea_a_actualizar.model_dump(exclude_defaults=True,
                                          exclude_none=True,
                                          exclude_unset=True,)
    if datos is None:
        raise HTTPException(status_code=400, detail="No se proporcionaron datos para actualizar")
    values = []

    datos["id"] = id
    for key, value in datos.items():
        values.append(value)

    set_str = ""

    for key, value in data.items():
        if value is not None:

            set_str += f"{key} = ?, "

    set_str = set_str[:-2]

    query = "UPDATE tareas SET " + set_str + " WHERE id = ?"
    print(query)
    print(values)
    cursor.execute(query, (values))
    db.commit()
    return tarea_final
@router.delete("/tareas/{id}")
def eliminar_tarea(id: int, db = Depends(database.get_db))-> Tarea:
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tareas WHERE id = ?", (id, ))
    resultado = cursor.fetchone()
    if resultado is None:
        raise HTTPException(status_code=404, detail=" Tarea no encontrada")

    cursor.execute("DELETE FROM tareas WHERE id = ?", (id,))
    db.commit()

    return Tarea(id=resultado["id"],
                 nombre=resultado["titulo"],
                 descripcion=resultado["descripcion"],
                 fecha=resultado["fecha"],
                 estado=resultado["estado"],
                 category_id=resultado["category_id"]
                 )








