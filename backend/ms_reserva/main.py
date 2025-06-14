import uvicorn
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests, os, uuid, csv
from pydantic import BaseModel

app = FastAPI()

ITINERARIOS_URL = "http://localhost:8001/itinerarios"
RESERVAS_CSV = "reservas.csv"
PAGAMENTO_URL = "http://localhost:8002/gerar-link"

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

class ReservaRequest(BaseModel):
    nome_navio: str
    destino: str
    data_embarque: str
    qtd_passageiros: int
    qtd_cabines: int

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
        return {"erro": "Erro ao consultar itinerários", str: str(e)}
    
@app.post("/reservar")
def criar_reserva(req: ReservaRequest):
    resp = requests.get("http://localhost:8001/detalhes-itinerario", params={
        "destino": req.destino,
        "nome_navio": req.nome_navio,
        "data": req.data_embarque
    })

    if resp.status_code != 200:
        raise HTTPException(status_code=404, detail="Itinerário não encontrado")

    dados = resp.json()
    cabines_disponiveis = dados.get("cabines_disponiveis")
    valor_por_pessoa = dados.get("valor_por_pessoa")

    if cabines_disponiveis < req.qtd_cabines:
        raise HTTPException(status_code=400, detail="Cabines insuficientes")

    valor_total = valor_por_pessoa * req.qtd_passageiros

    pagamento_resp = requests.post(PAGAMENTO_URL, json={
        "valor": valor_total
    })

    if pagamento_resp.status_code != 200:
        raise HTTPException(status_code=502, detail="Falha ao gerar link de pagamento")

    link_pagamento = pagamento_resp.json().get("link_pagamento")

    reserva_id = str(uuid.uuid4())
    nova_linha = [
        reserva_id,
        req.destino,
        req.nome_navio,
        req.data_embarque,
        req.qtd_passageiros,
        req.qtd_cabines,
        valor_total,
        link_pagamento
    ]

    file_exists = os.path.isfile(RESERVAS_CSV)
    with open(RESERVAS_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["reserva_id", "destino", "navio", "data", "passageiros", "cabines", "valor_total", "link_pagamento"])
        writer.writerow(nova_linha)

    return {
        "reserva_id": reserva_id,
        "valor_total": valor_total,
        "link_pagamento": link_pagamento
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)