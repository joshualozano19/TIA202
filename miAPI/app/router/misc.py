import asyncio
from typing import Optional
from fastapi import APIRouter

misc = APIRouter(tags=["Varios"])

@misc.get("/")
async def holamundo(): 
    return {"mensaje": "Hola mundo FastAPI"}

@misc.get("/bienvenido")
async def bienvenido():
    await asyncio.sleep(5)
    return {
        "mensaje": "Bienvenido a FastAPI",
        "estatus": "200",
    }

@misc.get("/v1/parametro0b/{id}")
async def consultauno(id: int):
    return {"mensaje":"usuario encontrado",
            "usuario": id,
            "status": "200"}

router = APIRouter(
    prefix="/v1/misc",
    tags=["Misceláneo"]
)

@router.get("/")
async def holamundo(): 
    return {"mensaje": "Hola mundo FastAPI"}

@router.get("/bienvenido")
async def bienvenido(): 
    await asyncio.sleep(2)
    return {"mensaje": "Bienvenido a FastAPI"}

# Rutas con Parámetros
@router.get("/usuario/detalles")
async def detalles(nombre: str, edad: int):
    return {
        "nombre": nombre, 
        "edad": edad,
        "mensaje": f"Hola {nombre}, tienes {edad} años."
    }

@router.get("/multiplicar/{numero}")
async def multiplicar(numero: int, multiplicador: Optional[int] = 2):
    resultado = numero * multiplicador
    return {
        "numero": numero,
        "multiplicador": multiplicador,
        "resultado": resultado
    }
