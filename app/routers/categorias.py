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
        categorias.append(Categoria(id=fila["id"], titulo_categoria=fila["titulo_categoria"]))


    return categorias

@router.get("/categorias/{id}")
def get_categoria(id: int, db = Depends(database.get_db_postgresql))-> Categoria:
    cursor = db.cursor()
    cursor.execute("SELECT * FROM categorias WHERE id = %s", (id,))
    resultado = cursor.fetchone()
    if resultado is None:
        raise HTTPException(status_code=404, detail="Categoria no existe")

    return Categoria(id=id, titulo_categoria=resultado["titulo_categoria"])

@router.post("/categorias")
def crear_categoria(categoria: CrearCategoria, db=Depends(database.get_db_postgresql))-> Categoria:
    cursor = db.cursor()
    cursor.execute("INSERT INTO categorias (titulo_categoria) VALUES (%s) RETURNING id", (categoria.titulo_categoria,))
    fetch_ans = cursor.fetchone()

    db.commit()
    return Categoria(id=fetch_ans["id"], titulo_categoria=categoria.titulo_categoria)
@router.patch("/categorias/{id}")
def actualizar_categoria(id: int, actualizarCategoria: ActualizarCategoria, db=Depends(database.get_db_postgresql))-> Categoria:
    cursor = db.cursor()
    cursor.execute("SELECT * FROM categorias WHERE id = %s", (id,))
    resultado = cursor.fetchone()
    if resultado is None:
        raise HTTPException(status_code=404, detail="Categoria no existe")

    cursor.execute("UPDATE categorias SET titulo_categoria = %s WHERE id = %s", (actualizarCategoria.titulo_categoria, id))
    db.commit()
    return Categoria(id=id, titulo_categoria=actualizarCategoria.titulo_categoria)

@router.delete("/categorias{id}")
def eliminar_categoria(id: int, db=Depends(database.get_db_postgresql))-> Categoria:
    cursor = db.cursor()
    cursor.execute("SELECT * FROM categorias WHERE id = %s ", (id,))
    resultado = cursor.fetchone()
    if resultado is None:
        raise HTTPException(status_code=404, detail="Categoria no existe")

    cursor.execute("DELETE FROM categorias WHERE id = %s", (id,))
    db.commit()

    return Categoria(id=id, titulo_categoria=resultado["titulo_categoria"])

