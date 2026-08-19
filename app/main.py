from fastapi import FastAPI

#from app.events_listener import revisarFechaExpirada
from app.redis.redis_client import start_redis
from app.routers.tareas import router as tareas_router
from app.routers.categorias import router as categorias_router
from app.routers.plantillas import router as plantillas_router
app = FastAPI()
app.include_router(tareas_router)
app.include_router(categorias_router)
app.include_router(plantillas_router)
@app.get("/")
def read_root():
    start_redis()
    return {"Working :)"}

#revisarFechaExpirada()