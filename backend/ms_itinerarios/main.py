import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from itinerarios import escutar_fila
from threading import Thread
from routes import router

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

app.include_router(router, prefix="/itinerarios", tags=["Itinerários"])

if __name__ == "__main__":
    Thread(target=escutar_fila, args=("reserva-criada", )).start()
    Thread(target=escutar_fila, args=("reserva-cancelada", )).start()
    uvicorn.run(app, host="0.0.0.0", port=8000)