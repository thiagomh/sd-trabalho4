import json
import os


def carregar_itinerarios():
    base_path = os.path.dirname(__file__)
    path = os.path.join(base_path, "itinerarios.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def listar_itinerarios():
    itinerarios = carregar_itinerarios()
    print("\n=== Itinerários Disponíveis ===")
    for id_it, i in itinerarios.items():
        print(f"ID: {id_it}")
        print(f"Destino: {i.get('destino', '-')}")
        print(f"Datas de Partida Disponíveis: {', '.join(i['datas'].keys())}")
        print(f"Navio: {i['nome_navio']}")
        print(f"Porto de Embarque: {i['portos_embarque']}")
        print(f"Lugares visitados: {', '.join(i['lugares_visitados'])}")
        print(f"Número de noites: {i['noites']}")
        print(f"Valor por pessoa: R$ {i['valor_por_pessoa']}")
        print()


def consultar_itinerarios(destino, data_embarque, porto):
    itinerarios = carregar_itinerarios()

    resultados = []
    for id_it, i in itinerarios.items():
        if (destino.lower() in i.get('destino', '').lower() and
            data_embarque in i.get('datas', {}) and
            porto.lower() in i.get('portos_embarque', '').lower()):
            resultados.append((id_it, i))

    if not resultados:
        print("\nNenhum itinerário encontrado com esses critérios.")
        return []

    print("\n=== Itinerários Encontrados ===")
    for id_it, i in resultados:
        print(f"ID: {id_it}")
        print(f"Destino: {i.get('destino', '-')}")
        print(f"Datas de Partida Disponíveis: {', '.join(i['datas'].keys())}")
        print(f"Navio: {i['nome_navio']}")
        print(f"Porto de Embarque: {i['portos_embarque']}")
        print(f"Lugares visitados: {', '.join(i['lugares_visitados'])}")
        print(f"Número de noites: {i['noites']}")
        print(f"Valor por pessoa: R$ {i['valor_por_pessoa']}")
        print()

    return resultados

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

