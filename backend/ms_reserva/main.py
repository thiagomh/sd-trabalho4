import uvicorn
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

ITINERARIOS_URL = "http://localhost:8001/itinerarios"

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

@app.get("/consulta-itinerarios")
def consulta_itinerarios(destino: str = Query(...), data_embarque: str = Query(...), porto_embarque: str = Query(...)):
    try:
        response = requests.get(ITINERARIOS_URL, params={
            "destino": destino,
            "data_embarque": data_embarque,
            "porto_embarque": porto_embarque
        })
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"erro": "Erro ao consultar itinerários", "detalhes": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)