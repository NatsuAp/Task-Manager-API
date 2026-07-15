from pydantic import BaseModel

class actualizarTarea(BaseModel):
    titulo: str | None = None
    descripcion: str | None = None
    fecha: str | None = None
    estado: str | None = None
    category_id: int | None = None

tarea = actualizarTarea(estado="Completado", descripcion="Estado de la Tarea")

l = []

l = tarea.model_dump(exclude_defaults=True)
keys = l.keys()
i = 0
for key in keys:
    print(key + " " + l[key])

