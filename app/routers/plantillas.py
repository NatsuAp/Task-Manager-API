from fastapi import APIRouter
from app.schemas import Plantilla, CrearPlantilla
from fastapi import Depends, HTTPException
import app.database_postgresql as database
router = APIRouter()

@router.get("/plantillas")
def get_plantillas(category_id: int, db = Depends(database.get_db_postgresql)) -> list[Plantilla]:
    cursor = db.cursor()

    query = "SELECT * FROM plantillas"

    if category_id is not None:
        query += " WHERE category_id = %s"

    cursor.execute(query, (category_id,))
    plantillas = cursor.fetchall()
    plantillas = []
    for plantilla in plantillas:
        plantillas.append(Plantilla(**plantilla))

    return plantillas

@router.get("/plantillas/{id}")
def get_plantilla(id: int, db = Depends(database.get_db_postgresql)) -> Plantilla:
    cursor = db.cursor()
    query = "SELECT * FROM plantillas WHERE id = %s"
    cursor.execute(query, (id,))
    plantilla = cursor.fetchone()

    return Plantilla(**plantilla)

@router.post("/plantillas")
def crear_plantilla(crearPlantilla: CrearPlantilla, db = Depends(database.get_db_postgresql)) -> Plantilla:
    cursor = db.cursor()

