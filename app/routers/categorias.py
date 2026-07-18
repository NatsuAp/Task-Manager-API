from fastapi import APIRouter, Depends
#import app.database_sqlite as database
import app.database_postgresql as database
from app.schemas import Categoria, CrearCategoria, ActualizarCategoria
from fastapi import HTTPException
router = APIRouter()


@router.get("/categorias")
def get_categorias(db = Depends(database.get_db_postgresql))-> list[Categoria]:
    categorias = []
    cursor = db.cursor()
    cursor.execute("SELECT * FROM categorias")
    resultados = cursor.fetchall()
    for fila in resultados:
        categorias.append(Categoria(id=fila["id"], nombre=fila["titulo"]))


    return categorias

@router.get("/categorias/{id}")
def get_categoria(id: int, db = Depends(database.get_db_postgresql))-> Categoria:
    cursor = db.cursor()
    cursor.execute("SELECT * FROM categorias WHERE id = %s", (id,))
    resultado = cursor.fetchone()
    if resultado is None:
        raise HTTPException(status_code=404, detail="Categoria no existe")

    return Categoria(id=id, nombre=resultado["titulo"])

@router.post("/categorias")
def crear_categoria(categoria: CrearCategoria, db=Depends(database.get_db_postgresql))-> Categoria:
    cursor = db.cursor()
    cursor.execute("INSERT INTO categorias (titulo) VALUES (%s) RETURNING id", (categoria.nombre,))
    fetch_ans = cursor.fetchone()
    
    db.commit()
    return Categoria(id=fetch_ans["id"], nombre=categoria.nombre)
@router.patch("/categorias/{id}")
def actualizar_categoria(id: int, actualizarCategoria: ActualizarCategoria, db=Depends(database.get_db_postgresql))-> Categoria:
    cursor = db.cursor()
    cursor.execute("SELECT * FROM categorias WHERE id = %s", (id,))
    resultado = cursor.fetchone()
    if resultado is None:
        raise HTTPException(status_code=404, detail="Categoria no existe")

    cursor.execute("UPDATE categorias SET titulo = %s WHERE id = %s", (actualizarCategoria.titulo, id))
    db.commit()
    return Categoria(id=id, nombre=actualizarCategoria.titulo)

@router.delete("/categorias{id}")
def eliminar_categoria(id: int, db=Depends(database.get_db_postgresql))-> Categoria:
    cursor = db.cursor()
    cursor.execute("SELECT * FROM categorias WHERE id = %s ", (id,))
    resultado = cursor.fetchone()
    if resultado is None:
        raise HTTPException(status_code=404, detail="Categoria no existe")

    cursor.execute("DELETE FROM categorias WHERE id = %s", (id,))
    db.commit()

    return Categoria(id=id, nombre=resultado["titulo"])

