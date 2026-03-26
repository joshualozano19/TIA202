from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.models.usuario import CrearUsuario, PatchUsuario
from app.security.auth import verificar_peticion

from app.data.db import get_db 
from app.data.usuario import usuario as dbUsuario

router = APIRouter(
    prefix="/v1/usuarios",
    tags=["HTTP CRUD"]
)

# 1. Leer todos (GET)
@router.get("/")
async def leer_usuarios(db: Session = Depends(get_db)):
    queryUsuarios = db.query(dbUsuario).all()
    return {
        "status": "200",
        "total": len(queryUsuarios),
        "usuarios": queryUsuarios
    }

# 2. Crear (POST)
@router.post("/", status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuarioP: CrearUsuario, db: Session = Depends(get_db)):
    nuevoU = dbUsuario(nombre=usuarioP.nombre, edad=usuarioP.edad)
    db.add(nuevoU)
    db.commit()
    db.refresh(nuevoU)
    return {"mensaje": "Usuario Agregado", "Usuario": nuevoU}

# 3. Actualizar completo (PUT)
@router.put("/{usuario_id}")
async def actualizar_usuario(usuario_id: int, usuarioP: CrearUsuario, db: Session = Depends(get_db)):
    res = db.query(dbUsuario).filter(dbUsuario.id == usuario_id).first()
    if not res:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    res.nombre = usuarioP.nombre
    res.edad = usuarioP.edad
    db.commit()
    db.refresh(res)
    return {"mensaje": "Usuario Actualizado", "datos": res}

# 4. Actualizar parcial (PATCH)
@router.patch("/{usuario_id}")
async def actualizar_usuario_parcial(usuario_id: int, datos_parciales: PatchUsuario, db: Session = Depends(get_db)):
    res = db.query(dbUsuario).filter(dbUsuario.id == usuario_id).first()
    if not res:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    cambios = datos_parciales.model_dump(exclude_unset=True)
    for key, value in cambios.items():
        setattr(res, key, value)
    
    db.commit()
    db.refresh(res)
    return {"mensaje": "Usuario actualizado parcialmente", "usuario": res}

# 5. Eliminar (DELETE)
@router.delete("/{usuario_id}")
async def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db), usuario_Auth: str = Depends(verificar_peticion)):
    res = db.query(dbUsuario).filter(dbUsuario.id == usuario_id).first()
    if not res:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db.delete(res)
    db.commit()
    return {"mensaje": "Usuario eliminado", "eliminado_por": usuario_Auth}