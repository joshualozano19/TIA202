from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, Field
from datetime import date
from typing import List, Optional

app = FastAPI()

class Reservation(BaseModel):
    id: int
    name: str
    time: str = Field(..., gt="08:00", lt="22:00")
    day: str
    month: str
    year: int
    personas: int

class huesped(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str] = None

class Habitacion(BaseModel):
    id: int
    type: str
    price: float
    available: bool


reservations: List[Reservation] = []
huespeds: List[huesped] = []
habitaciones: List[Habitacion] = []

@app.post("/reservations/", status_code=status.HTTP_201_CREATED)
def create_reservation(reservation: Reservation):
    if any(r.day == "Domingo" for r in reservations):
        raise HTTPException(status_code=400, detail="No se pueden hacer reservas los domingos.")

    reservations.append(reservation)
    return reservation