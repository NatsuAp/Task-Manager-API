from fastapi import APIRouter, Depends
import app.database as database
from app.schemas import Categoria, CrearCategoria

router = APIRouter()


@router.get("/categorias")
def get_categorias(db = Depends(database.get_db))-> list[Categoria]:
    categorias = []
    cursor = db.cursor()
    cursor.execute("SELECT * FROM categorias")
    resultados = cursor.fetchall()
    for fila in resultados:
        categorias.append(Categoria(id=fila["id"], nombre=fila["titulo"]))


    return categorias

@router.post("/categorias")
def crear_categoria(categoria: CrearCategoria, db=Depends(database.get_db))-> Categoria:
    cursor = db.cursor()
    cursor.execute("INSERT INTO categorias (titulo) VALUES (?)", (categoria.nombre,))
    db.commit()
    return Categoria(id=cursor.lastrowid, nombre=categoria.nombre)

#TODO: DELETE ENDPOINT para elimnar categorias, me toca definir si al eliminar una categoria,
# se eliminan las tareas que dependan de ella, o cambio la categoria a "Tablero" o alguna generica
@router.delete("/categorias{id}")
def eliminar_categoria()

