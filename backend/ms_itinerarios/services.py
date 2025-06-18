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
            "cabines_disponiveis": it["datas"][data_embarque]["cabines_disponiveis"],
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
            
    raise HTTPException(status_code=404, detail="Nenhum itinerário encontrado com os filtros informados.")
    # return {"erro": "Itinerário não encontrado"}


def atualizar_cabines_disponiveis(nome_navio, data_embarque, quantidade, operacao):
    base_path = os.path.dirname(__file__)
    path = os.path.join(base_path, "database.json")
    with open(path, "r", encoding="utf-8") as f:
        itinerarios = json.load(f)

    id_encontrado = None
    for id_itinerario, dados in itinerarios.items():
        if dados.get("nome_navio") == nome_navio:
            id_encontrado = id_itinerario
            break

    if not id_encontrado:
        print(f"Navio '{nome_navio}' não encontrado.")
        return False

    itinerario = itinerarios[id_encontrado]
    datas = itinerario.get("datas", {})

    if data_embarque not in datas:
        print(f"Data '{data_embarque}' não encontrada para o navio '{nome_navio}'.")
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

    with open(path, "w", encoding="utf-8") as f:
        json.dump(itinerarios, f, indent=4, ensure_ascii=False)

    print(f"Cabines atualizadas e arquivo salvo para navio '{nome_navio}' na data '{data_embarque}'.")
    return True

