"""Inventario de red — Práctica 4.
Alumno:    Maqueda Cruz Mariela
Matrícula: 125054826
"""
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(title="Inventario de red")


class Dispositivo(BaseModel):
    nombre: str
    tipo: str
    ip: str
    activo: bool = True


class DispositivoParcial(BaseModel):
    nombre: str | None = None
    tipo: str | None = None
    ip: str | None = None
    activo: bool | None = None


inventario = [
    Dispositivo(nombre="R1", tipo="router", ip="10.0.0.1"),
    Dispositivo(nombre="SW1", tipo="switch", ip="10.0.0.10", activo=False),
    Dispositivo(nombre="FW1", tipo="firewall", ip="10.0.0.254"),
]


def buscar(nombre: str):
    """Busca un dispositivo por nombre (sin importar mayúsculas/minúsculas)."""
    for eq in inventario:
        if eq.nombre.upper() == nombre.upper():
            return eq
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No existe el equipo: {nombre}"
    )


# ─── RUTAS ───

@app.get("/")
async def estado():
    """Comprueba que el servicio responde."""
    return {"servicio": "Inventario de red", "total": len(inventario)}


@app.get("/dispositivos")
async def listar(activo: bool | None = None):
    """Lista todos los dispositivos. Filtra con ?activo=true o ?activo=false."""
    if activo is None:
        return inventario
    return [eq for eq in inventario if eq.activo == activo]


@app.post("/dispositivos", status_code=status.HTTP_201_CREATED)
async def crear(equipo: Dispositivo):
    """Agrega un nuevo dispositivo al inventario."""
    try:
        buscar(equipo.nombre)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe el equipo: {equipo.nombre}"
        )
    except HTTPException as e:
        if e.status_code == 404:
            inventario.append(equipo)
            return equipo
        raise


@app.get("/dispositivos/{nombre}")
async def obtener(nombre: str):
    """Consulta un dispositivo por su nombre."""
    return buscar(nombre)


@app.put("/dispositivos/{nombre}")
async def reemplazar(nombre: str, datos: Dispositivo):
    """Reemplaza TODOS los datos de un dispositivo existente."""
    eq = buscar(nombre)
    eq.nombre = datos.nombre
    eq.tipo = datos.tipo
    eq.ip = datos.ip
    eq.activo = datos.activo
    return eq


@app.patch("/dispositivos/{nombre}")
async def modificar(nombre: str, datos: DispositivoParcial):
    """Modifica SOLO los campos enviados de un dispositivo."""
    eq = buscar(nombre)
    if datos.nombre:
        eq.nombre = datos.nombre
    if datos.tipo:
        eq.tipo = datos.tipo
    if datos.ip:
        eq.ip = datos.ip
    if datos.activo is not None:
        eq.activo = datos.activo
    return eq


@app.delete("/dispositivos/{nombre}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar(nombre: str):
    """Elimina un dispositivo del inventario."""
    eq = buscar(nombre)
    inventario.remove(eq)
