from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import random
import requests
from threading import Thread
import uvicorn
from pydantic import BaseModel

app = FastAPI()

WEBHOOK_URL = "http://localhost:8002/notificacao"

pagamentos = {}

class CriarLinkRequest(BaseModel):
    reserva_id: str
    valor: float
    moeda: str
    cliente_nome: str
    cliente_email: str

@app.post("/criar-link")
def criar_link(req: CriarLinkRequest):
    reserva_id = req.reserva_id
    valor = req.valor
    cliente_nome = req.cliente_nome if req.cliente_nome else "Não identificado"
    cliente_email = req.cliente_email if req.cliente_email else "naoinformado@email.com"

    link = f"http://localhost:8005/pagar/{reserva_id}"

    def enviar_webhook():
        status = random.choice([True, False])

        payload = {
            "id_transacao": f"txn_{random.randint(1000,9999)}",
            "reserva_id": reserva_id,
            "status": status,
            "valor": valor,
            "cliente": {
                "nome": cliente_nome,
                "email": cliente_email
            }
        }

        pagamentos[reserva_id] = payload

        try:
            print(f"[Sistema Externo] Enviando webhook: {payload}")
            requests.post(WEBHOOK_URL, json=payload)
        except Exception as e:
            print(f"[Erro ao enviar webhook]: {e}")

    Thread(target=enviar_webhook).start()

    return {"link_pagamento": link}

@app.get("/pagar/{reserva_id}", response_class=HTMLResponse)
async def visualizar_pagamento(reserva_id: str):
    dados = pagamentos.get(reserva_id)
    if not dados:
        return HTMLResponse("<h2>Reserva não encontrada.</h2>", status_code=404)

    status = "✅ Pagamento Aprovado" if dados["status"] else "❌ Pagamento Recusado"
    cor_status = "green" if dados["status"] else "red"

    html = f"""
    <html>
    <head>
        <title>Pagamento da Reserva</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f8f9fa;
                padding: 40px;
            }}
            .card {{
                background: white;
                padding: 30px;
                border-radius: 10px;
                max-width: 500px;
                margin: auto;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }}
            h2 {{
                color: #2c3e50;
            }}
            p {{
                font-size: 18px;
                margin: 10px 0;
            }}
            .status {{
                font-weight: bold;
                color: {cor_status};
                font-size: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <h2>Detalhes do Pagamento</h2>
            <p><strong>ID da Transação:</strong> {dados["id_transacao"]}</p>
            <p><strong>Reserva ID:</strong> {reserva_id}</p>
            <p><strong>Cliente:</strong> {dados["cliente"]["nome"]}</p>
            <p><strong>Email:</strong> {dados["cliente"]["email"]}</p>
            <p><strong>Valor:</strong> R$ {dados["valor"]:.2f}</p>
            <p class="status">{status}</p>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html)

if __name__ == "__main__":
    print("SISTEMA EXTERNO PAGAMENTO")
    uvicorn.run(app, host="0.0.0.0", port=8005)