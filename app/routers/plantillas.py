import psycopg2
from fastapi import APIRouter
from app.schemas import Plantilla, CrearPlantilla, ActualizarPlantilla
from fastapi import Depends, HTTPException
from psycopg2.extras import Json
import app.database_postgresql as database


router = APIRouter()

@router.get("/plantillas")
def get_plantillas(category_id: int | None = None, db = Depends(database.get_db_postgresql)) -> list[Plantilla]:
    cursor = db.cursor()

    query = "SELECT * FROM plantillas"
    params = ()
    if category_id is not None:
        query += " WHERE category_id = %s"
        params = (category_id,)
    cursor.execute(query, params)
    plantillas = cursor.fetchall()
    lista_plantillas = []

    for plantilla in plantillas:
        lista_plantillas.append(Plantilla(id=plantilla['id'],
                                          titulo_plantilla=plantilla['titulo_plantilla'],
                                          category_id=plantilla['category_id'],
                                          campos=plantilla['campos'],
                                          es_default=plantilla['es_default']))

    return lista_plantillas

@router.get("/plantillas/{id}")
def get_plantilla(id: int, db = Depends(database.get_db_postgresql)) -> Plantilla:
    cursor = db.cursor()
    query = "SELECT * FROM plantillas WHERE id = %s"
    cursor.execute(query, (id,))

    plantilla = cursor.fetchone()
    if plantilla is None:
        raise HTTPException(status_code=404, detail= "Plantilla no existe")
    return Plantilla(id=plantilla['id'],
                     titulo_plantilla=plantilla['titulo_plantilla'],
                     category_id=plantilla['category_id'],
                     campos=plantilla['campos'],
                     es_default=plantilla['es_default'])


@router.post("/plantillas")
def crear_plantilla(crearPlantilla: CrearPlantilla, db = Depends(database.get_db_postgresql)) -> Plantilla:
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO plantillas (titulo_plantilla, category_id, campos, es_default) "
                       "VALUES (%s, %s, %s, FALSE) RETURNING id", (crearPlantilla.titulo_plantilla, crearPlantilla.category_id, Json(crearPlantilla.campos),))
    except psycopg2.errors.ForeignKeyViolation: #Si funciona
        db.rollback()
        raise HTTPException(status_code=400, detail= "Una categoria con ese id no existe")

    db.commit()
    fetch_ans = cursor.fetchone()
    print(fetch_ans)
    return Plantilla(id=fetch_ans['id'],
                     titulo_plantilla=crearPlantilla.titulo_plantilla,
                     category_id=crearPlantilla.category_id,
                     campos=crearPlantilla.campos,
                     es_default=False)

# class ActualizarPlantilla(BaseModel):
#     titulo_plantilla: str | None = None
#     category_id: int | None = None
#     campos: dict[str, str] | None = None
@router.patch("/plantillas/{id}")
def actualizar_plantilla(id: int, actualizarPlantilla : ActualizarPlantilla, db = Depends(database.get_db_postgresql)) -> Plantilla:
    cursor = db.cursor()

    cursor.execute("SELECT * FROM plantillas WHERE id = %s", (id,))
    plantilla_vieja = cursor.fetchone()
    if plantilla_vieja is None:
        raise HTTPException(status_code=404, detail= "Plantilla no existe")

    plantilla_final_dict = {
        'titulo_plantilla': plantilla_vieja['titulo_plantilla'],
        'category_id': plantilla_vieja['category_id'],
        'campos': plantilla_vieja['campos']
    }

    datos_nuevos = actualizarPlantilla.model_dump(exclude_defaults=True,
                                          exclude_none=True,
                                          exclude_unset=True)
    print("Datos nuevos: " + str(datos_nuevos))

    for key, value in datos_nuevos.items():
        plantilla_final_dict[key] = value

    values = []
    set_params = ""
    for key, value in plantilla_final_dict.items():
        set_params += key + " = %s, "
        if isinstance(value, dict):
            values.append(Json(value))
        else:
            values.append(value)

    set_params = set_params[:-2]

    values.append(id)
    query = "UPDATE plantillas SET " + set_params + " WHERE id = %s"

    cursor.execute(query, (values))

    db.commit()

    return Plantilla(id= id,
                     titulo_plantilla=plantilla_final_dict['titulo_plantilla'],
                     category_id=plantilla_final_dict['category_id'],
                     campos=plantilla_final_dict['campos'],
                     es_default=False)

@router.delete("/plantillas/{id}")
def eliminar_plantilla(id: int, db = Depends(database.get_db_postgresql)) -> Plantilla:
    cursor = db.cursor()
    cursor.execute("SELECT * FROM plantillas WHERE id = %s", (id,))
    plantilla = cursor.fetchone()
    if plantilla is None:
        raise HTTPException(status_code=404, detail= "Plantilla no existe")

    cursor.execute("DELETE FROM plantillas WHERE id = %s", (id,))
    db.commit()
    return Plantilla(**plantilla)







