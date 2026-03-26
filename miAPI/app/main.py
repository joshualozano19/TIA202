from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.router.usuario import router as usuario_router
from app.router.misc import router as misc_router
from app.router import usuario,misc
from app.data.db import engine


from app.data.db import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Mi API con FastAPI",
    description="Angel Joshua Guerrero Lozano",
    version="1.0.0"

)

app.include_router(usuario_router)
app.include_router(misc_router)