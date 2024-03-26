# import data_base
# from model import Db_information
import requests
import json
# db = Db_information("Termometria",3306,"192.168.15.50","scada","termometria")
# conn = data_base.Connector(db)

# data = conn.select_data_placa_secun()

# resultado_agrupado = {}
# # Agrupando os dados pelo canal_placa

# for item in data:
#     canal = item['canal_placa']
#     id_sensor = item['sensor_placa']
#     if canal not in resultado_agrupado:
#         resultado_agrupado[canal] = [id_sensor]
#     else:
#         resultado_agrupado[canal].append(id_sensor)
# # Convertendo o dicionário para a lista desejada
        

lista_final = [{1:[1,2,3,4,5]},{2:[1,2,3,4,5]},{3:[1,2,3,4,5]}]

url = 'http://192.168.15.51/api/teste/'

# Fazendo a solicitação POST com um corpo de solicitação JSON
response = requests.post(url, json=lista_final)

# Exibindo a resposta
#response = response.json()


if response.status_code == 200:
    # Capturar o conteúdo da resposta
    response_content = response.text
    print('Conteúdo da resposta:', response_content)
else:
    print('Ocorreu um erro ao fazer a solicitação POST:', response.text)


