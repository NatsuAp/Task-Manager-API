
from fastapi import HTTPException
from app.schemas import CrearTarea, Tarea, ActualizarTarea
#import app.database_sqlite as database
import app.database_postgresql as database
from fastapi import Depends, APIRouter

router = APIRouter()

@router.post("/tareas")
def crear_tarea(tarea: CrearTarea, db = Depends(database.get_db_postgresql)) -> Tarea:
    print(tarea.nombre)
    cursor = db.cursor()
    estado = 'Pendiente'
    cursor.execute("SELECT * FROM categorias WHERE id = %s", (tarea.category_id,))
    resultado = cursor.fetchone()

    if resultado is None:
        raise HTTPException(status_code=404, detail="Categoria con ese ID no existe")



    cursor.execute("insert into tareas (titulo_tarea, descripcion, fecha, estado, category_id) values (%s, %s, %s, %s, %s) RETURNING id", (tarea.nombre, tarea.descripcion, tarea.fecha, estado, tarea.category_id))
    db.commit()
    fetch_ans = cursor.fetchone()


    return Tarea(id=fetch_ans["id"],
                 nombre=tarea.nombre,
                 descripcion=tarea.descripcion,
                 fecha=tarea.fecha,
                 estado= estado,
                 category_id=tarea.category_id)

#Enpoint, parametro opcional para filtrar por category_id
@router.get("/tareas")
def get_tareas(category_id: int | None = None, db = Depends(database.get_db_postgresql))-> list[Tarea]:

    cursor = db.cursor()

    query = ("SELECT tareas.id, tareas.titulo_tarea, tareas.descripcion, tareas.fecha, tareas.estado, tareas.category_id, categorias.titulo_categoria "
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
                            nombre=tarea["titulo_tarea"],
                            descripcion=tarea["descripcion"],
                            fecha=tarea["fecha"],
                            estado=tarea["estado"],
                            category_id=tarea["category_id"]))

    return tareas

@router.get("/tareas/{id}")
def get_tarea(id: int, db = Depends(database.get_db_postgresql)) -> Tarea:
    cursor = db.cursor()

    cursor.execute("SELECT * FROM tareas WHERE id = %s", (id,))
    resultado = cursor.fetchone()
    if resultado is None:
        raise HTTPException(status_code=404, detail=" Tarea no encontrada")

    return Tarea(id=resultado["id"],
                 nombre=resultado["titulo_tarea"],
                 descripcion=resultado["descripcion"],
                 fecha=resultado["fecha"],
                 estado=resultado["estado"],
                 category_id=resultado["category_id"])

@router.patch("/tareas/{id}")
def actualizar_tarea(id: int, tarea_a_actualizar: ActualizarTarea, db = Depends(database.get_db_postgresql)) -> Tarea:

    cursor = db.cursor()
    cursor.execute("SELECT * FROM tareas WHERE id = %s", (id,))
    resultado = cursor.fetchone()
    if resultado is None:
        raise HTTPException(status_code=404, detail=" Tarea no encontrada")

    tarea_final_dict = {
        "id": resultado["id"],
        "nombre": resultado["titulo_tarea"],
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
        set_str += f"{key} = %s, "
    values.append(id)
    set_str = set_str[:-2]

    query = "UPDATE tareas SET " + set_str + " WHERE id = %s"
    print(query)
    print(values)
    cursor.execute(query, (values))
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

    return Tarea(id=resultado["id"],
                 nombre=resultado["titulo_tarea"],
                 descripcion=resultado["descripcion"],
                 fecha=resultado["fecha"],
                 estado=resultado["estado"],
                 category_id=resultado["category_id"]
                 )








