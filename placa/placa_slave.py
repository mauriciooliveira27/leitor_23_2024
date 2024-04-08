from model import Db_information
import json
from leitor_termo import Leitor_temp
from multiplex import Multiplex3
import time
from datetime import date
from datetime import datetime
from model import registro_instalacao
import requests
import threading
import traceback
from .placa_abs import PlacaAbstract
import data_base

class DataPlacaSlaves:

    def get_data_placa(self, data):
        cod_placa       =   [cod['cod_placa'] for cod in data]
        ip_placa        =   [ip['ip'] for ip in data]
        return cod_placa  , ip_placa




class PlacaSlave(PlacaAbstract, DataPlacaSlaves):

    def __init__(self) -> None:
        self.db                     =       Db_information("Termometria",3306,"localhost","leitor_termo","termometria")
        self.conn                   =       data_base.Connector(self.db)
        self.conf                   =       self.conn.get_informaton_instal()
        self.data_instal            =       json.loads(self.conf.dados)
        self.leitor                 =       Leitor_temp()
        self.mp                     =       Multiplex3()
        self.dt                     =       datetime
        self.read_temp              =       True
        self.registro_instal        =       registro_instalacao(0, self.conf.nome, self.conf.configuracao_fisica, self.dt.now(), "")
        self.result_placa_slave       =       None
        self.lock                   =       threading.RLock()
        
    



    def read_temp(self, data_placa: object) -> dict:
        print('PLACA SECUNDARIA')
        with self.lock:
            self.result_placa_secund    =       self.conn.select_data_placa_secun()
        
        cod_placa,ip_placa      =   self.get_data_placa(self.result_placa_secund)

        resultado_agrupado      =   {}#agrupando em dicionario os canal e sensores EX: {1:[1,2,3,4,5]}
        chave_cordoes           =   []#salvo em lista os nomes dos cordeos fisicos EX: 'Ch1S1'
        data_placa              =   None
        data_temp               =   {}

        for indice, cod in enumerate(cod_placa):
            data_placa = self.conn.select_data_placa_secun(cod) #pega os dados da placa
        
            for item in data_placa:
                canal           =   item['canal_placa']#pega canal 
                id_sensor       =   item['sensor_placa']#pega o sensor
                chave_cordoes.append(item['cordao_fisico'])#pego nomes dos cordoes fisicos

                if canal not in resultado_agrupado:
                    resultado_agrupado[canal] = [id_sensor]#cria o dicionario , caso a chave 'canal" ainda não exista , caso contrario ele apenas adiciona o sensor a lista na linha 97
                else:
                    resultado_agrupado[canal].append(id_sensor)

            lista_final         =   [{canal:sensores} for canal , sensores in resultado_agrupado.items()]#cria lista de dicionario [{1:[1,2,3,4,5]},{2:[1,2,3,4,5]},{3:[1,2,3,4,5]}] a api espera essa estrutura
            ip                  =   ip_placa[indice]
            erro = 0
            print(ip)
            while erro < 3:
                try:
                    url                 =   f'http://{ip}/api/get_temp/'
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
                    time.sleep(30)

                except Exception as e:
                  
                    erro += 1
                    print('Erro:', e)
                    print('dentro do except')
                    print(erro)
                    print(f"Erro: {type(e).__name__} - {e}")
                    print("Traceback (linha onde ocorreu o erro):")
                    traceback.print_exc()
                    time.sleep(30)

                if erro == 3:
                    self.result_placa_secund = {chave: '' for chave in chave_cordoes }
                    break