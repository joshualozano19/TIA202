from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, Field
from datetime import date
from typing import List, Optional

app = FastAPI(title = "Biblioteca Digital UPQ")

class Libro(BaseModel):
    id: int
    titulo: str = Field(..., min_length=2, max_length=100)
    autor: str
    paginas: int = Field(..., gt=1)
    anio: int = Field(..., gt=1450, lt=date.today().year)
    estado: str = "disponible"

class Usuario(BaseModel):
    nombre: str = Field(..., min_length=3)
    correo: str

class RegistroPrestamo(BaseModel):
    id_libro: int
    usuario: Usuario
    fecha_prestamo: date = date.today()

libros_db = []
prestamos_db = []

@app.get("/libros/", tags=["Biblioteca"])
async def listar_libros():
    return {"total": len(libros_db), "libros": libros_db}

@app.post("/libros", status_code=status.HTTP_201_CREATED, tags=["Biblioteca"])
async def crear_libro(libro: Libro):
    for l in libros_db:
        if l.id == libro.id or l.titulo.lower() == libro.titulo.lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El ID o el libro ya existen"
            )
    libros_db.append(libro)
    return {"mensaje": "Libro creado exitosamente", "libro": libro}

@app.get("/libros/buscar/{nombre}", tags=["Biblioteca"])
async def buscar_libro(nombre: str):
    if len(nombre) < 2:
        raise HTTPException(status_code=400, detail="Nombre de búsqueda demasiado corto")
    
    for libro in libros_db:
        if libro.titulo.lower() == nombre.lower():
            return libro
        
    raise HTTPException(status_code=404, detail="Libro no encontrado")

@app.put("/libros/prestar/{id_libro}", tags=["Biblioteca"])
async def prestar_libro(id_libro: int, usuario: Usuario):
    for libro in libros_db:
        if libro.id == id_libro:
            if libro.estado == "prestado":
                raise HTTPException(status_code=409, detail="El libro ya está prestado")
            libro.estado = "prestado"

            nuevo_prestamo = RegistroPrestamo(id_libro=id_libro, usuario=usuario)
            prestamos_db.append(nuevo_prestamo)
            return {"mensaje": "Préstamo registrado exitosamente", "libro": nuevo_prestamo}
    raise HTTPException(status_code=404, detail="Libro no encontrado")

@app.put("/libros/devolver/{id}", tags=["Biblioteca"])
async def devolver_libro(id: int):
    for libro in libros_db:
        if libro.id == id:
            libro.estado = "disponible"
            return {"mensaje": "Libro devuelto exitosamente", "libro": libro}
        
    raise HTTPException(status_code=404, detail="Libro no encontrado")
    
@app.delete("/libros/eliminar-prestamo/{id_libro}", tags=["Biblioteca"])
async def eliminar_prestamo(id_libro: int):
    for registro in prestamos_db:
        if registro.id_libro == id_libro:
            prestamos_db.remove(registro)
            
            for libro in libros_db:
                if libro.id == id_libro:
                    libro.estado = "disponible"
                return {"mensaje": "Préstamo eliminado y libro disponible", "libro": libro}
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail="El registro de préstamo no existe"
            )