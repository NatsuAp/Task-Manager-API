
from fastapi import HTTPException
from app.schemas import CrearTarea, Tarea, ActualizarTarea
#import app.database_sqlite as database
import app.database_postgresql as database
from fastapi import Depends, APIRouter
import json
from psycopg2.extras import Json
from sentry_sdk.utils import json_dumps

router = APIRouter()

@router.post("/tareas")
def crear_tarea(tarea: CrearTarea, db = Depends(database.get_db_postgresql)) -> Tarea:

    cursor = db.cursor()
    estado = 'Pendiente'
    cursor.execute("SELECT * FROM categorias WHERE id = %s", (tarea.category_id,))
    resultado = cursor.fetchone()

    if resultado is None:
        raise HTTPException(status_code=404, detail="Categoria con ese ID no existe")


    campos = None
    if tarea.template_id is not None:
        cursor.execute("SELECT campos FROM plantillas WHERE id = %s AND category_id = %s", (tarea.template_id, tarea.category_id))
        campos_query = cursor.fetchone()
        if campos_query is None:
            raise HTTPException(status_code=404, detail="plantilla no existe")

        campos = campos_query["campos"]

    if tarea.campos is not None and campos is not None:
        tarea.campos = campos | tarea.campos
    elif campos is not None:
        tarea.campos = campos





        cursor.execute("insert into tareas (titulo_tarea, descripcion, fecha, estado, category_id, template_id, campos) "
                   "values (%s, %s, %s, %s, %s, %s, %s) RETURNING id",
                   (tarea.titulo_tarea, tarea.descripcion, tarea.fecha, estado, tarea.category_id, tarea.template_id, Json(tarea.campos)))

    db.commit()
    fetch_ans = cursor.fetchone()


    return Tarea(id=fetch_ans["id"],
                 titulo_tarea=tarea.titulo_tarea,
                 descripcion=tarea.descripcion,
                 fecha=tarea.fecha,
                 estado= estado,
                 category_id=tarea.category_id,
                 template_id=tarea.template_id,
                 campos= tarea.campos)

#Enpoint, parametro opcional para filtrar por category_id
@router.get("/tareas")
def get_tareas(category_id: int | None = None, db = Depends(database.get_db_postgresql))-> list[Tarea]:

    cursor = db.cursor()

    query = ("SELECT tareas.id, "
             "tareas.titulo_tarea, "
             "tareas.descripcion, "
             "tareas.fecha, "
             "tareas.estado, "
             "tareas.category_id, "
             "tareas.template_id, "
             "tareas.campos, "
             "categorias.titulo_categoria "
             "FROM tareas INNER JOIN categorias ON tareas.category_id = categorias.id")
    #query += "INNER JOIN categorias ON tareas.category_id = categorias.id"
    params = ()
    if category_id is not None:
        query += " WHERE category_id = %s"
        params = (category_id,)
    query += " ORDER BY tareas.id ASC"
    cursor.execute(query, params)

    #TODO: la variable resultado contiene la columna unida de categorias "titulo_categoria" pero no se guarda al momento de retornar la lista tareas
    # puesto que el esquema de tareas no tiene una variable que guarde el nombre de la categoria, actualmente solo el id de la categoria,
    # tocaria añadir una nueva variable al esquema y cambiar todos los endpoints donde se utilice este para que funcione debidamente

    resultados = cursor.fetchall()
    tareas = []
    for tarea in resultados:
        #cursor.execute("SELECT titulo FROM categorias  WHERE id = %s", (category_id,))
        tareas.append(Tarea(id=tarea["id"],
                            titulo_tarea=tarea["titulo_tarea"],
                            descripcion=tarea["descripcion"],
                            fecha=tarea["fecha"],
                            estado=tarea["estado"],
                            category_id=tarea["category_id"],
                            template_id=tarea["template_id"],
                            campos = tarea["campos"]))

    return tareas

@router.get("/tareas/{id}")
def get_tarea(id: int, db = Depends(database.get_db_postgresql)) -> Tarea:
    cursor = db.cursor()

    cursor.execute("SELECT * FROM tareas WHERE id = %s", (id,))
    resultado = cursor.fetchone()
    if resultado is None:
        raise HTTPException(status_code=404, detail=" Tarea no encontrada")

    return Tarea(**resultado)

@router.patch("/tareas/{id}")
def actualizar_tarea(id: int, tarea_a_actualizar: ActualizarTarea, db = Depends(database.get_db_postgresql)) -> Tarea:

    cursor = db.cursor()
    cursor.execute("SELECT * FROM tareas WHERE id = %s", (id,))
    resultado = cursor.fetchone()
    if resultado is None:
        raise HTTPException(status_code=404, detail=" Tarea no encontrada")

    tarea_final_dict = {
        "id": resultado["id"],
        "titulo_tarea": resultado["titulo_tarea"],
        "descripcion": resultado["descripcion"],
        "fecha": resultado["fecha"],
        "estado": resultado["estado"],
        "category_id": resultado["category_id"],
        "template_id": resultado["template_id"],
        "campos": Json(resultado["campos"])
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
        if isinstance(value, dict):
            values.append(Json(value))
        else:
            values.append(value)
        set_str += f"{key} = %s, "
    values.append(id)
    set_str = set_str[:-2]

    query = "UPDATE tareas SET " + set_str + " WHERE id = %s"
    print(query)
    print(*values, sep="###")
    cursor.execute(query, values)
    db.commit()
    return tarea_final
@router.delete("/tareas/{id}")
def eliminar_tarea(id: int, db = Depends(database.get_db_postgresql))-> Tarea:
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tareas WHERE id = %s", (id, ))
    resultado = cursor.fetchone()
    if resultado is None:
        raise HTTPException(status_code=404, detail=" Tarea no encontrada")

    cursor.execute("DELETE FROM tareas WHERE id = %s", (id,))
    db.commit()

    return Tarea(**resultado)








