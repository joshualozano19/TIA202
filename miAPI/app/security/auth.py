from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

security = HTTPBasic()

def verificar_peticion(credenciales:HTTPBasicCredentials=Depends(security)):
    usuario_correcto=secrets.compare_digest(credenciales.username,"AxelSantiago")
    contrasena_correcta=secrets.compare_digest(credenciales.password,"123456")

    if not(usuario_correcto and contrasena_correcta):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="credenciales no validas"
        )
    return credenciales.username