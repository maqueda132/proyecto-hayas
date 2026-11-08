"""Práctica 4 - Alumna: Maqueda Cruz Mariela - Matrícula: 125054826"""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(title="Inventario de red")
class Dispositivo(BaseModel):
    nombre: str
    tipo: str
    ip: str
    activo: bool = True
inventario = [
    Dispositivo(nombre="R1", tipo="router", ip="10.0.0.1"),
]
@app.post("/dispositivos", status_code=status.HTTP_201_CREATED, summary="Crear un nuevo dispositivo")
def crear_dispositivo(dispositivo: Dispositivo):
    for d in inventario:
        if d.nombre == dispositivo.nombre:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe el equipo: {dispositivo.nombre}"
            )
    inventario.append(dispositivo)
    return dispositivo
