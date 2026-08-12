import psycopg2
from fastapi import APIRouter
from app.schemas import Plantilla, CrearPlantilla, ActualizarPlantilla
from fastapi import Depends, HTTPException
from psycopg2.extras import Json
import app.database.database_postgresql as database
from app.redis.redis_client import redis_client
import json
from app.config import CACHE_TTL
from pydantic import BaseModel

router = APIRouter()

@router.get("/plantillas")
def get_plantillas(category_id: int | None = None, db = Depends(database.get_db_postgresql)) -> list[Plantilla]:
    key = "plantillas"
    if category_id is not None:
        key = key + f"_c_{category_id}"
    cache = redis_client.get(key)
    if cache is not None:
        datos = json.loads(cache)
        plantillas = []
        for dato in datos:
            plantillas.append(Plantilla(**dato))

        print("Entro en cache")
        return plantillas


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
    redis_client.set(key, json.dumps([c.model_dump() for c in lista_plantillas]), ex=CACHE_TTL)
    return lista_plantillas

@router.get("/plantillas/{id}")
def get_plantilla(id: int, db = Depends(database.get_db_postgresql)) -> Plantilla:
    #cache redis
    cache = redis_client.get(f'plantillas_{id}')
    if cache is not None:
        datos = json.loads(cache)
        print("Entro en cache")
        return Plantilla(**datos)

    #query normal
    cursor = db.cursor()
    query = "SELECT * FROM plantillas WHERE id = %s"
    cursor.execute(query, (id,))

    resultado = cursor.fetchone()
    if resultado is None:
        raise HTTPException(status_code=404, detail= "Plantilla no existe")
    plantilla = Plantilla(id=resultado['id'],
                     titulo_plantilla=resultado['titulo_plantilla'],
                     category_id=resultado['category_id'],
                     campos=resultado['campos'],
                     es_default=resultado['es_default'])
    redis_client.set(f'plantillas_{id}', json.dumps(plantilla.model_dump()), ex=CACHE_TTL)

    return plantilla

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
    #print(fetch_ans)
    #unlink es lo mismo que delete pero asincrono

    for key in redis_client.scan_iter(match='plantillas*'):
        redis_client.unlink(key)

    return Plantilla(id=fetch_ans['id'],
                     titulo_plantilla=crearPlantilla.titulo_plantilla,
                     category_id=crearPlantilla.category_id,
                     campos=crearPlantilla.campos,
                     es_default=False)

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
    for key in redis_client.scan_iter(match='plantillas*'):
        redis_client.unlink(key)

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
    for key in redis_client.scan_iter(match='plantillas*'):
        redis_client.unlink(key)

    return Plantilla(**plantilla)

