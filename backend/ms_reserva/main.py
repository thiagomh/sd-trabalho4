import uvicorn
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests, os, uuid, csv
from pydantic import BaseModel
from reserva import publicar_reserva, escutar_fila, callback_aprovado, callback_recusado, callback_bilhete
import time
from threading import Thread

app = FastAPI()

ITINERARIOS_URL = "http://localhost:8001/itinerarios"
PAGAMENTO_URL = "http://localhost:8002/gerar-link"
RESERVAS_CSV = "reservas.csv"

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
    print("Recebido:", req.dict())
    resp = requests.get("http://localhost:8001/detalhes-itinerario", params={
        "destino": req.destino,
        "nome_navio": req.nome_navio,
        "data": req.data_embarque
    })

    if resp.status_code != 200:
        raise HTTPException(status_code=404, detail="Itinerário não encontrado")

    dados = resp.json()
    cabines_disponiveis = int(dados.get("cabines_disponiveis"))
    valor_por_pessoa = int(dados.get("valor_por_pessoa"))

    if cabines_disponiveis < req.qtd_cabines:
        raise HTTPException(status_code=400, detail="Cabines insuficientes")

    valor_total = valor_por_pessoa * req.qtd_passageiros

    reserva_id = str(time.time())
    pagamento_resp = requests.post(PAGAMENTO_URL, json={
        "valor": valor_total,
        "reserva_id": reserva_id,
        "moeda": "BRL",
        "cliente": {
            "nome": "",
            "email": ""
        }
    })

    if pagamento_resp.status_code != 200:
        raise HTTPException(status_code=502, detail="Falha ao gerar link de pagamento")

    link_pagamento = pagamento_resp.json().get("link_pagamento")

    status = "ativa"
    nova_linha = [
        reserva_id,
        req.destino,
        req.nome_navio,
        req.data_embarque,
        req.qtd_passageiros,
        req.qtd_cabines,
        valor_total,
        link_pagamento,
        status
    ]

    base_path = os.path.dirname(__file__)
    path = os.path.join(base_path, "reservas.csv")
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(nova_linha)

    try:
        publicar_reserva(
            id_reserva=reserva_id,
            nome_navio=req.nome_navio,           
            data_embarque=req.data_embarque,
            passageiros=req.qtd_passageiros,
            cabines=req.qtd_cabines,
            routing_key='reserva-criada',
        )
    except Exception as e:
        print(f"Erro ao publicar mensagem na fila: {e}")

    return {
        "reserva_id": reserva_id,
        "valor_total": valor_total,
        "link_pagamento": link_pagamento
    }

@app.delete("/reservar/{codigo}")
def cancelar_reserva(codigo: str):
    print(f"Cancelando reserva com código: {codigo}")
    reserva_encontrada = False
    reservas_atualizadas = []
    base_path = os.path.dirname(__file__)
    path = os.path.join(base_path, "reservas.csv")

    try:
        with open(path, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames:
                raise ValueError("Cabeçalhos do CSV não encontrados.")
            fieldnames = reader.fieldnames

            for row in reader:
                if row["id"] == codigo:
                    print(f"Reserva encontrada: {row}")
                    row["status"] = "cancelada"
                    reserva_encontrada = True

                    try:
                        publicar_reserva(
                            id_reserva=row["id"],
                            nome_navio=row["nome_navio"],
                            data_embarque=row["data_embarque"],
                            passageiros=row["qtd_passageiros"],
                            cabines=row["qtd_cabines"],
                            routing_key='reserva-cancelada'
                        )
                    except Exception as e:
                        print(f"Erro ao publicar mensagem: {e}")

                reservas_atualizadas.append(row)

        if not reserva_encontrada:
            return {"erro": f"Reserva com código {codigo} não encontrada"}

        with open(path, "w", newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(reservas_atualizadas)

        print(f"Reserva {codigo} cancelada com sucesso.")
        return {"mensagem": f"Reserva {codigo} cancelada com sucesso"}
    
    except Exception as e:
        print(f"Erro ao processar cancelamento: {e}")
        raise HTTPException(status_code=500, detail="Erro interno no servidor")

if __name__ == "__main__":
    print("=== MS RESERVA ===")
    Thread(target=escutar_fila, args=('pagamento-aprovado', callback_aprovado)).start()
    Thread(target=escutar_fila, args=('pagamento-recusado', callback_recusado)).start()
    Thread(target=escutar_fila, args=('bilhete-gerado', callback_bilhete)).start()
    uvicorn.run(app, host="0.0.0.0", port=8000)