# import data_base
# from model import Db_information
import requests
import json
from placa import PlacaMaster
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
        

# lista_final = [{1: [1, 2]}, 
#                {2: [1,]}, 
#           ]

# url = 'http://192.168.15.51/api/get_temp/'

# # Fazendo a solicitação POST com um corpo de solicitação JSON
# response = requests.post(url, json=lista_final)

# # Exibindo a resposta
# #response = response.json()


# if response.status_code == 200:
#     # Capturar o conteúdo da resposta
#     response_content = response.text
#     print('Conteúdo da resposta:', response_content)
# else:
#     print('Ocorreu um erro ao fazer a solicitação POST:', response.text)


# VALOR = ["31.98","32.30","32.09","31.95","32.05","32.10","32.10","32.02","32.23","32.24","31.76","32.19","33.44","33.45","33.51","33.41","33.93","33.98","33.93","34.00","34.02","33.97","33.98","33.95","33.99","33.97","34.00","34.09","32.88","32.91","32.98","32.98","34.77","34.72","34.72","34.87","34.75","34.81","34.82","34.79","34.75","34.81","34.81","34.84","34.09","34.07","33.93","34.07","34.61","34.51","34.52","34.61","34.52","34.59","34.52","34.71","34.64","34.59","34.59","34.55","34.95","34.87","34.91","34.90","32.91","32.94","33.14","32.68","33.11","32.96","32.72","32.93","32.86","33.16","32.70","32.98","32.38","32.38","32.33","32.46","34.02","34.12","33.95","34.02","33.95","34.09","34.23","34.04","34.02","34.06","34.09","34.14","33.27","33.30","33.40","33.30","35.45","33.40","33.39","33.35","35.16","33.27","33.48","33.53","33.39","33.59","33.23","35.28","35.25","35.12","35.21","35.38","33.37","33.35","33.21","33.27","33.23","33.12","33.39","33.30","33.46","33.34","33.30","33.44","33.48","33.52","33.49","33.55","33.79","33.72","33.60","33.42","33.78","33.61","33.76","33.74","33.78","33.77","33.78","33.84","33.92","34.09","33.93","33.97","34.28","34.35","34.46","34.38","34.41","34.35","34.35","34.41","34.34","34.53","34.52","34.48","34.60","34.51","34.66","34.48","32.63","32.72","32.55","32.70","32.52","32.52","32.63","32.80","32.79","32.67","32.70","32.63","34.34","34.35","34.28","34.23","32.47","32.45","32.84","32.44","32.51","32.52","32.61","32.38","32.52","31.94","32.44","32.49","33.92","33.97","33.95","33.93","41.39","41.49","41.53","41.60","41.52","41.52","41.60","41.60","41.61","41.55","41.53","41.63","34.56","34.66","34.60","34.48","33.70","33.59","33.79","33.74","33.59","33.61","33.84","33.65","33.79","33.58","33.77","33.78","33.40","33.62","33.40","33.45","33.88","34.06","34.05","34.16","34.06","34.16","34.20","34.16","34.16","34.19","34.02","34.06","33.23","33.00","33.25","33.07","37.33","37.35","37.28","37.26","37.35","37.39","37.37","37.25","37.53","37.25","37.34","37.39","32.33","32.23","32.33","32.22"]

# CHAVE = ['Ch17S1', 'Ch17S2', 'Ch17S3', 'Ch17S4', 'Ch17S5', 'Ch17S6', 'Ch17S7', 'Ch17S8', 'Ch17S9', 'Ch17S10', 'Ch17S11', 'Ch17S12', 'Ch17S13', 'Ch17S14', 'Ch17S15', 'Ch17S16', 'Ch18S1', 'Ch18S2', 'Ch18S3', 'Ch18S4', 'Ch18S5', 'Ch18S6', 'Ch18S7', 'Ch18S8', 'Ch18S9', 'Ch18S10', 'Ch18S11', 'Ch18S12', 'Ch18S13', 'Ch18S14', 'Ch18S15', 'Ch18S16', 'Ch19S1', 'Ch19S2', 'Ch19S3', 'Ch19S4', 'Ch19S5', 'Ch19S6', 'Ch19S7', 'Ch19S8', 'Ch19S9', 'Ch19S10', 'Ch19S11', 'Ch19S12', 'Ch19S13', 'Ch19S14', 'Ch19S15', 'Ch19S16', 'Ch20S1', 'Ch20S2', 'Ch20S3', 'Ch20S4', 'Ch20S5', 'Ch20S6', 'Ch20S7', 'Ch20S8', 'Ch20S9', 'Ch20S10', 'Ch20S11', 'Ch20S12', 'Ch20S13', 'Ch20S14', 'Ch20S15', 'Ch20S16', 'Ch21S1', 'Ch21S2', 'Ch21S3', 'Ch21S4', 'Ch21S5', 'Ch21S6', 'Ch21S7', 'Ch21S8', 'Ch21S9', 'Ch21S10', 'Ch21S11', 'Ch21S12', 'Ch21S13', 'Ch21S14', 'Ch21S15', 'Ch21S16', 'Ch22S1', 'Ch22S2', 'Ch22S3', 'Ch22S4', 'Ch22S5', 'Ch22S6', 'Ch22S7', 'Ch22S8', 'Ch22S9', 'Ch22S10', 'Ch22S11', 'Ch22S12', 'Ch22S13', 'Ch22S14', 'Ch22S15', 'Ch22S16', 'Ch23S1', 'Ch23S2', 'Ch23S3', 'Ch23S4', 'Ch23S5', 'Ch23S6', 'Ch23S7', 'Ch23S8', 'Ch23S9', 'Ch23S10', 'Ch23S11', 'Ch23S12', 'Ch23S13', 'Ch23S14', 'Ch23S15', 'Ch23S16', 'Ch24S1', 'Ch24S2', 'Ch24S3', 'Ch24S4', 'Ch24S5', 'Ch24S6', 'Ch24S7', 'Ch24S8', 'Ch24S9', 'Ch24S10', 'Ch24S11', 'Ch24S12', 'Ch24S13', 'Ch24S14', 'Ch24S15', 'Ch24S16', 'Ch25S1', 'Ch25S2', 'Ch25S3', 'Ch25S4', 'Ch25S5', 'Ch25S6', 'Ch25S7', 'Ch25S8', 'Ch25S9', 'Ch25S10', 'Ch25S11', 'Ch25S12', 'Ch25S13', 'Ch25S14', 'Ch25S15', 'Ch25S16', 'Ch26S1', 'Ch26S2', 'Ch26S3', 'Ch26S4', 'Ch26S5', 'Ch26S6', 'Ch26S7', 'Ch26S8', 'Ch26S9', 'Ch26S10', 'Ch26S11', 'Ch26S12', 'Ch26S13', 'Ch26S14', 'Ch26S15', 'Ch26S16', 'Ch27S1', 'Ch27S2', 'Ch27S3', 'Ch27S4', 'Ch27S5', 'Ch27S6', 'Ch27S7', 'Ch27S8', 'Ch27S9', 'Ch27S10', 'Ch27S11', 'Ch27S12', 'Ch27S13', 'Ch27S14', 'Ch27S15', 'Ch27S16', 'Ch28S1', 'Ch28S2', 'Ch28S3', 'Ch28S4', 'Ch28S5', 'Ch28S6', 'Ch28S7', 'Ch28S8', 'Ch28S9', 'Ch28S10', 'Ch28S11', 'Ch28S12', 'Ch28S13', 'Ch28S14', 'Ch28S15', 'Ch28S16', 'Ch29S1', 'Ch29S2', 'Ch29S3', 'Ch29S4', 'Ch29S5', 'Ch29S6', 'Ch29S7', 'Ch29S8', 'Ch29S9', 'Ch29S10', 'Ch29S11', 'Ch29S12', 'Ch29S13', 'Ch29S14', 'Ch29S15', 'Ch29S16', 'Ch30S1', 'Ch30S2', 'Ch30S3', 'Ch30S4', 'Ch30S5', 'Ch30S6', 'Ch30S7', 'Ch30S8', 'Ch30S9', 'Ch30S10', 'Ch30S11', 'Ch30S12', 'Ch30S13', 'Ch30S14', 'Ch30S15', 'Ch30S16', 'Ch31S1', 'Ch31S2', 'Ch31S3', 'Ch31S4', 'Ch31S5', 'Ch31S6', 'Ch31S7', 'Ch31S8', 'Ch31S9', 'Ch31S10', 'Ch31S11', 'Ch31S12', 'Ch31S13', 'Ch31S14', 'Ch31S15', 'Ch31S16', 'Ch32S1', 'Ch32S2', 'Ch32S3', 'Ch32S4', 'Ch32S5', 'Ch32S6', 'Ch32S7', 'Ch32S8', 'Ch32S9', 'Ch32S10', 'Ch32S11', 'Ch32S12', 'Ch32S13', 'Ch32S14', 'Ch32S15', 'Ch32S16']


# RESULTADO  = dict(zip(CHAVE,VALOR))
# print(VALOR.__class__)


# cod = [1,2,3,4]
# ip = ['192.168.15.51','192.168.15.52','192.168.15.53','192.168.15.54']

# for indice , c in enumerate(cod):
    
#     i = ip[indice]
#     print(f"cod{c} ip {i}")

# acumulado = {}
# r1 = {'ch1s1': '20.01'}
# acumulado.update(r1)
# r2 = {'ch2s2': '20.1'}
# acumulado.update(r2)
# r3 = {'ch3s3': '21.5'}
# acumulado.update(r3)


# print(acumulado)
from manager_placa import ManagerPlacaMaster
from manager_placa import ManagerPlacaSlave
app = PlacaMaster()

app.read_temp(ManagerPlacaMaster())

print(app.result_placa_master)

manage_slave = ManagerPlacaSlave()
print(manage_slave._ip_placa)