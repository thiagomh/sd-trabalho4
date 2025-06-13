from fastapi import APIRouter, Query
from pydantic import BaseModel
from backend.ms_reserva.services import consultar_itinerarios


router = APIRouter()

class ReservaRequest(BaseModel):
    id_itinerario = int
    data_embarque: str
    passageiros: int
    cabines: int

@router.get("/")
def buscar_itinerarios(destino: str = Query(...), data_embarque: str = Query(...), porto_embarque: str = Query(...)):
    return consultar_itinerarios(destino, data_embarque, porto_embarque)
