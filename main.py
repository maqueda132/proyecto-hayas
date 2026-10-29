from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI(title="Inventario de red")

# ---------------------------------------------------------------
# Modelos
# ---------------------------------------------------------------
class Dispositivo(BaseModel):
    """Representa un equipo del inventario."""
    nombre: str
    tipo: str
    ip: str
    activo: bool = True

    def apagar(self):
        self.activo = False

    def encender(self):
        self.activo = True

    def etiqueta(self) -> str:
        estado = "activo" if self.activo else "inactivo"
        return f"{self.nombre} ({self.tipo}) - {estado}"


class DispositivoActualizar(BaseModel):
    """Todos los campos opcionales: sirve para actualizaciones parciales."""
    tipo: str | None = None
    ip: str | None = None
    activo: bool | None = None


# ---------------------------------------------------------------
# Datos iniciales
# ---------------------------------------------------------------
inventario = [
    Dispositivo(nombre="R1", tipo="router", ip="10.0.0.1"),
    Dispositivo(nombre="SW1", tipo="switch", ip="10.0.0.10", activo=False),
    Dispositivo(nombre="FW1", tipo="firewall", ip="10.0.0.254"),
]


def buscar(nombre: str) -> Dispositivo:
    """Devuelve el equipo o lanza un 404."""
    for equipo in inventario:
        if equipo.nombre.upper() == nombre.upper():
            return equipo
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No existe el equipo {nombre}",
    )


# ---------------------------------------------------------------
# RUTA PARA MOSTRAR TODOS LOS MÉTODOS — Lo que pide la tarea
# ---------------------------------------------------------------
@app.get("/metodos", summary="Lista todos los métodos disponibles")
async def listar_metodos() -> List[Dict]:
    """Devuelve cada método, su ruta y descripción."""
    return [
        {
            "metodo": "POST",
            "ruta": "/dispositivos",
            "descripcion": "Crear dispositivo (CREATE)"
        },
        {
            "metodo": "GET",
            "ruta": "/dispositivos",
            "descripcion": "Listar todos los dispositivos (READ)"
        },
        {
            "metodo": "GET",
            "ruta": "/dispositivos/{nombre}",
            "descripcion": "Consultar un dispositivo por nombre (READ)"
        },
        {
            "metodo": "PUT",
            "ruta": "/dispositivos/{nombre}",
            "descripcion": "Reemplazar todos los datos (UPDATE completo)"
        },
        {
            "metodo": "PATCH",
            "ruta": "/dispositivos/{nombre}",
            "descripcion": "Modificar solo algunos campos (UPDATE parcial)"
        },
        {
            "metodo": "DELETE",
            "ruta": "/dispositivos/{nombre}",
            "descripcion": "Eliminar dispositivo (DELETE)"
        },
        {
            "metodo": "GET",
            "ruta": "/metodos",
            "descripcion": "Muestra esta lista de métodos"
        }
    ]


# ---------------------------------------------------------------
# CRUD — Rutas principales
# ---------------------------------------------------------------
@app.post("/dispositivos", status_code=status.HTTP_201_CREATED)
async def crear(equipo: Dispositivo):
    """Crear un nuevo dispositivo."""
    for existente in inventario:
        if existente.nombre.upper() == equipo.nombre.upper():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe el equipo {equipo.nombre}",
            )
    inventario.append(equipo)
    return equipo


@app.get("/dispositivos")
async def listar(activo: bool | None = None):
    """Listar todos los dispositivos, filtro opcional por estado."""
    if activo is None:
        return inventario
    return [equipo for equipo in inventario if equipo.activo == activo]


@app.get("/dispositivos/{nombre}")
async def obtener(nombre: str):
    """Consultar un dispositivo por su nombre."""
    return buscar(nombre)


@app.put("/dispositivos/{nombre}")
async def reemplazar(nombre: str, datos: Dispositivo):
    """Reemplazar todos los datos del dispositivo."""
    equipo = buscar(nombre)
    equipo.tipo = datos.tipo
    equipo.ip = datos.ip
    equipo.activo = datos.activo
    return equipo


@app.patch("/dispositivos/{nombre}")
async def modificar(nombre: str, datos: DispositivoActualizar):
    """Modificar solo los campos enviados."""
    equipo = buscar(nombre)
    cambios = datos.model_dump(exclude_unset=True)
    for campo, valor in cambios.items():
        setattr(equipo, campo, valor)
    return equipo


@app.delete("/dispositivos/{nombre}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar(nombre: str):
    """Eliminar un dispositivo del inventario."""
    equipo = buscar(nombre)
    inventario.remove(equipo)