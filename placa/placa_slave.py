from model import Db_information
import json
import time
import requests
import traceback
from .placa_abs import PlacaAbstract
import data_base
from model import Db_information
import data_base


class PlacaSlave(PlacaAbstract):

    def __init__(self, ip_placa, cod_placa) -> None:
        self.ip_placa = ip_placa
        self.cod_placa = cod_placa
        self.result_placa_secund = None

    def __str__(self) -> str:
        return 'Iniciando leitura Placa-Slave' + f'{self.ip_placa}'
    

    def read_temp(self):
        resultado_agrupado      =   {}#agrupando em dicionario os canal e sensores EX: {1:[1,2,3,4,5]}
        chave_cordoes           =   []#salvo em lista os nomes dos cordeos fisicos EX: 'Ch1S1'
        data_placa              =   None
        data_temp               =   {}
        self.db                 =   Db_information("Termometria",3306,"localhost","leitor_termo","termometria")
        self.conn               =   data_base.Connector(self.db)
        data_placa              =   self.conn.select_data_placa_secun(self.cod_placa) #pega os dados da placa
        for item in data_placa:
                canal           =   item['canal_placa']#pega canal 
                id_sensor       =   item['sensor_placa']#pega o sensor
                chave_cordoes.append(item['cordao_fisico'])#pego nomes dos cordoes fisicos

                if canal not in resultado_agrupado:
                    resultado_agrupado[canal] = [id_sensor]#cria o dicionario , caso a chave 'canal" ainda não exista , caso contrario ele apenas adiciona o sensor a lista na linha 97
                else:
                    resultado_agrupado[canal].append(id_sensor)

        lista_final         =   [{canal:sensores} for canal , sensores in resultado_agrupado.items()]#cria lista de dicionario [{1:[1,2,3,4,5]},{2:[1,2,3,4,5]},{3:[1,2,3,4,5]}] a api espera essa estrutura
        erro = 0
        print(self.ip_placa)
        while erro < 1:
            try:
                url                 =   f'http://{self.ip_placa}/api/get_temp/'
                response            =   requests.post(url, json=lista_final)   
                leituras            =   response.text
                status_cod          =   response.status_code

                if status_cod == 200:
                    leitura_list        =   json.loads(leituras)
                    response_content    =   dict(zip(chave_cordoes,leitura_list))
                    chave_cordoes.clear()
                    data_temp.update(response_content)
                    self.result_placa_secund = data_temp
                    break

                elif status_cod != 200:
                    erro += 1
                    print("DENTRO DO ELIF : STATUS_CODE != 200",)
                    time.sleep(30)

            except requests.exceptions.RequestException as e:
            
                erro += 1
                print('Erro de requisição:', e)
                print('dentro do except')
                print(erro)
                

            except Exception as e:
                
                erro += 1
                print('Erro:', e)
                print('dentro do except')
                print(erro)
                print(f"Erro: {type(e).__name__} - {e}")
                print("Traceback (linha onde ocorreu o erro):")
                traceback.print_exc()
                time.sleep(30)

            if erro == 1:
                self.result_placa_secund = {chave: '' for chave in chave_cordoes }
                break