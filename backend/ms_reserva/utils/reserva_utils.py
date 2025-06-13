import json 
import os
# ------------------------------------------------ 
# Carrega os itinerários de um arquivo .json
# ------------------------------------------------
def carregar_itinerarios():
      base_path = os.path.dirname(__file__)
      path = os.path.join(base_path, "database.json")
      print(path)
      with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

# ------------------------------------------------
# Consulta itinerários com os filtros do cliente
# ------------------------------------------------
def consultar_itinerarios(destino, data_embarque, porto):
    itinerarios = carregar_itinerarios()
    print("executei")

    destino = destino.strip().lower()
    porto = porto.strip().lower()
    data_embarque = data_embarque.strip()

    resultados = []

    for i in itinerarios.values():
        if (
            destino == i['destino'].strip().lower() and
            porto == i['portos_embarque'].strip().lower() and
            data_embarque in i['datas']
        ):
            resultados.append({
                "destino": i['destino'],
                "navio": i['nome_navio'],
                "porto_embarque": i['portos_embarque'],
                "data_embarque": data_embarque,
                "lugares_visitados": i['lugares_visitados'],
                "noites": i['noites'],
                "valor_por_pessoa": i['valor_por_pessoa'],
                "cabines_disponiveis": i['datas'][data_embarque]["cabines_disponiveis"]
            })

    if not resultados:
        print("\nNenhum itinerário encontrado com esses critérios.")
        return []

    print("\n=== Itinerários Encontrados ===")
    for i in resultados:
        print(f"Navio: {i['navio']}")
        print(f"Porto de Embarque: {i['porto_embarque']}")
        print(f"Data: {i['data_embarque']}")
        print(f"Lugares visitados: {', '.join(i['lugares_visitados'])}")
        print(f"Noites: {i['noites']}")
        print(f"Valor por pessoa: {i['valor_por_pessoa']}")
        print(f"Cabines disponíveis: {i['cabines_disponiveis']}")
        print()

    return resultados