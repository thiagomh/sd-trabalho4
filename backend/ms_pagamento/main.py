import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uuid
from pydantic import BaseModel
from pagamento import escutar_fila
from threading import Thread

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

class PagamentoRequest(BaseModel):
    valor: float

@app.post("/gerar-link")
def gerar_link_pagamento(req: PagamentoRequest):
    if req.valor <= 0:
        raise HTTPException(status_code=400, detail="Valor inválido")

    link = f"https://pagamento.com/pagar/{uuid.uuid4()}"
    
    return {"link_pagamento": link}

if __name__ == "__main__":
    Thread(target=escutar_fila, args=()).start()
    uvicorn.run(app, host="0.0.0.0", port=8002)