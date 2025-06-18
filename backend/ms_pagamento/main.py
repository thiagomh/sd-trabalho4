import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pagamento import escutar_fila, publica_na_fila
from threading import Thread
import requests

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
    reserva_id: str
    moeda: str = "BRL"
    cliente: dict

class NotificacaoPagamento(BaseModel):
    id_transacao: str
    status: bool  
    valor: float
    cliente: dict

@app.post("/gerar-link")
def gerar_link(req: PagamentoRequest):
    if req.valor <= 0:
        raise HTTPException(status_code=400, detail="Valor inválido")

    try:
        params = {
            "valor": req.valor,
            "reserva_id": req.reserva_id,
            "moeda": req.moeda,
            "cliente_nome": req.cliente["nome"],
            "cliente_email": req.cliente["email"]
        }
        response = requests.post("http://localhost:8005/criar-link", json=params)
        response.raise_for_status()
        return {"link_pagamento": response.json()["link_pagamento"]}
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Erro ao contatar sistema externo {str(e)}")
    
@app.post("/notificacao")
async def webhook_pagamento(request: Request):
    dados = await request.json()
    print("[MS Pagamento] Webhook recebido:", dados)

    status = dados.get("status")
    reserva_id = dados.get("reserva_id")

    fila = "pagamento-aprovado" if status else "pagamento-recusado"

    publica_na_fila(fila, dados)

    print(f"[MS Pagamento] Publicando mensagem: reserva {reserva_id} -> {status}")

    return {"mensagem": "Webhook processado com sucesso"} 



if __name__ == "__main__":
    print("=== MS PAGAMENTO ===")
    Thread(target=escutar_fila, args=()).start()
    uvicorn.run(app, host="0.0.0.0", port=8002)