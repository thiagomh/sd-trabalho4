from fastapi import APIRouter, Query
from services import listar_itinerarios, consultar_itinerarios

router = APIRouter()

@router.get("/")
def listar():
    return listar_itinerarios()

@router.get("/consulta")
def consultar(
    destino: str = Query(...),
    data_embarque: str = Query(...),
    porto_embarque: str = Query(...)
):
    return consultar_itinerarios(destino, data_embarque, porto_embarque)