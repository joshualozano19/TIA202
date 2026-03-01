#importaciones
from fastapi import FastAPI
import asyncio



#Instacia del servidor
app = FastAPI()



#Endpoints
@app. get("/")
async def hola_mundo():
    return {"mensaje": "Hola Mundo FastAPI"}
@app.get("/bienvenido")
async def bienvenido():
    return {"mensaje": "Bienvenido a FastAPI",
            "estatus": "200 OK"}