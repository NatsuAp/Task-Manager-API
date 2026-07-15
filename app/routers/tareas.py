from dns.name import empty
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
    cursor.execute("SELECT * FROM categorias WHERE id = ?", (tarea.category_id,))
    resultado = cursor.fetchone()
    if resultado is None:
        raise HTTPException(status_code=404, detail="Categoria con ese ID no existe")

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

    cursor = db.cursor()
    cursor.execute("SELECT * FROM tareas WHERE id = ?", (id,))
    resultado = cursor.fetchone()
    if resultado is None:
        raise HTTPException(status_code=404, detail=" Tarea no encontrada")

    tarea_final_dict = {
        "id": resultado["id"],
        "nombre": resultado["titulo"],
        "descripcion": resultado["descripcion"],
        "fecha": resultado["fecha"],
        "estado": resultado["estado"],
        "category_id": resultado["category_id"]
    }



    datos = tarea_a_actualizar.model_dump(exclude_defaults=True,
                                          exclude_none=True,
                                          exclude_unset=True,)
    for key, value in datos.items():
        tarea_final_dict[key] = value

    tarea_final = Tarea(**tarea_final_dict)
    if len(datos) == 0:
        raise HTTPException(status_code=400, detail="No se proporcionaron datos para actualizar")
    values = []

    set_str = ""

    for key, value in datos.items():
        values.append(value)
        set_str += f"{key} = ?, "
    values.append(id)
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








