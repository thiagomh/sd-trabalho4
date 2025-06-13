import uvicorn
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from itinerarios import escutar_fila, callback_cancelada, callback_criada
from services import consultar_itinerarios
from threading import Thread
from typing import Optional

app = FastAPI()

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/itinerarios")
def consultar(
    destino: Optional[str] = Query(None),
    data_embarque: Optional[str] = Query(None),
    porto_embarque: Optional[str] = Query(None)
):
    return consultar_itinerarios(destino, data_embarque, porto_embarque)

if __name__ == "__main__":
    Thread(target=escutar_fila, args=("reserva-criada", callback_criada)).start()
    Thread(target=escutar_fila, args=("reserva-cancelada", callback_cancelada)).start()
    uvicorn.run(app, host="0.0.0.0", port=8001)