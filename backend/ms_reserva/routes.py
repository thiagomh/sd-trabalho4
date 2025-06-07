from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter()

class ReservaRequest(BaseModel):
    id_itinerario = int
    data_embarque: str
    passageiros: int
    cabines: int


# @router.post("/")
# def reservar_cruzeiro(reserva: ReservaRequest):
#     return criar_reserva(reserva)