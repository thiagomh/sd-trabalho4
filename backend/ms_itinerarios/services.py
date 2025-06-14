import json
import os
from fastapi import HTTPException


def carregar_itinerarios():
    base_path = os.path.dirname(__file__)
    path = os.path.join(base_path, "database.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def consultar_itinerarios(destino, data_embarque, porto_embarque):
    itinerarios = carregar_itinerarios()

    resultados = []
    for id_, it in itinerarios.items():
        
        if destino and it["destino"].lower() != destino.lower():
            continue
        
       
        if porto_embarque and it["portos_embarque"].lower() != porto_embarque.lower():
            continue
        
        
        if data_embarque:
            if data_embarque not in it["datas"]:
                continue
            if it["datas"][data_embarque]["cabines_disponiveis"] <= 0:
                continue

        
        item_resposta = {
            "id": id_,
            "destino": it["destino"],
            "nome_navio": it["nome_navio"],
            "portos_embarque": it["portos_embarque"],
            "noites": it["noites"],
            "valor_por_pessoa": it["valor_por_pessoa"],
            "lugares_visitados": it["lugares_visitados"],
            "datas": it["datas"],
        }
        resultados.append(item_resposta)

    if not resultados:
        raise HTTPException(status_code=404, detail="Nenhum itinerário encontrado com os filtros informados.")

    return resultados

def consultar_detalhes(destino: str, nome_navio: str, data: str):
    itinerarios = carregar_itinerarios()
    for item in itinerarios.values():
            if (
                item["destino"] == destino
                and item["nome_navio"] == nome_navio
                and data in item["datas"]
            ):
                return {
                    "valor_por_pessoa": item["valor_por_pessoa"],
                    "cabines_disponiveis": item["datas"][data]["cabines_disponiveis"]
                }
    return {"erro": "Itinerário não encontrado"}


def atualizar_cabines_disponiveis(id_itinerario, data_embarque, quantidade, operacao):
    itinerarios = carregar_itinerarios()
    id_itinerario = str(id_itinerario)  
    if id_itinerario not in itinerarios:
        print(f"Itinerário {id_itinerario} não encontrado.")
        return False

    itinerario = itinerarios[id_itinerario]
    datas = itinerario.get("datas", {})

    if data_embarque not in datas:
        print(f"Data {data_embarque} não encontrada para o itinerário {id_itinerario}.")
        return False

    cabines_atuais = datas[data_embarque]["cabines_disponiveis"]

    if operacao == "criar":
        if quantidade > cabines_atuais:
            print("Erro: cabines insuficientes.")
            return False
        datas[data_embarque]["cabines_disponiveis"] -= quantidade

    elif operacao == "cancelar":
        datas[data_embarque]["cabines_disponiveis"] += quantidade

    else:
        print("Operação inválida. Use 'criar' ou 'cancelar'.")
        return False

    return True

