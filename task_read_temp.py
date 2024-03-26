import data_base
from model import Db_information
import json
from leitor_termo import Leitor_temp
from multiplex import Multiplex3
import time
from datetime import date
from datetime import datetime
from model import registro_instalacao
import requests

class App:
        
    def __init__(self) -> None:
        self.db                 =       Db_information("Termometria",3306,"localhost","leitor_termo","termometria")
        self.conn               =       data_base.Connector(self.db)
        self.conf               =       self.conn.get_informaton_instal()
        self.data_instal        =       json.loads(self.conf.dados)
        self.leitor             =       Leitor_temp()
        self.mp                 =       Multiplex3()
        self.dt                 =       datetime
        self.read_temp          =       True
        self.registro_instal    =       registro_instalacao(0, self.conf.nome, self.conf.configuracao_fisica, self.dt.now(), "")


    def exe_read_temp(self):

        data_placa                      =       self.conn.select_placa_main()
        resultado_agrupado              =       {}
        chave_cordoes                   =       []

        for item in data_placa:

            canal               =       item['canal_placa']
            id_sensor           =       item['sensor_placa']
            chave_cordoes.append(item['cordao_fisico'])

            if canal not in resultado_agrupado:
                resultado_agrupado[canal] = [id_sensor]
            else:
                resultado_agrupado[canal].append(id_sensor)

        # Convertendo o dicionário para a lista desejada
        lista_final     =       [{canal: sensores} for canal, sensores in resultado_agrupado.items()]
        leituras        =       []


        for canal in lista_final:
            canals              =       canal.keys()
            sensores            =       list(canal.values())
            sensores_list       =       sensores[0]
    
            #Set hardware channel and sensor
            for c in canal:
        
                for s in sensores_list:
                
                    c_int           =       int(c)
                    s_int           =       int(s)
                    self.mp.set_canal(c_int)
                    self.mp.set_sensor(s_int)
                    value_sensor    =       self.leitor.read_temp()
                    leituras.append(f'{value_sensor:.2f}')

            
        print(chave_cordoes)
        print(leituras)
        resultado                                       =   dict(zip(chave_cordoes, leituras))
        self.registro_instal.registros_temperaturas     =   json.dumps(resultado)
        self.registro_instal.data                       =   self.dt.now()
        self.conn.insert_registro_instalacao(self.registro_instal)


    def get_cod_placa(self):

        result          =   self.conn.select_placa_secund() 
        cod_placa       =   [cod['cod_placa'] for cod in result]
        ip_placa        =   [ip['ip'] for ip in result]
        return cod_placa  , ip_placa
    


    def read_temp_placa_secun(self):

        cod_placa,ip_placa      =   self.get_cod_placa()
        resultado_agrupado      =   {}#agrupando em dicionario os canal e sensores EX: {1:[1,2,3,4,5]}
        chave_cordoes           =   []#salvo em lista os nomes dos cordeos fisicos EX: 'Ch1S1'

        data_placa = None
        for cod in cod_placa:
            data_placa = self.conn.select_data_placa_secun(cod) #pega os dados da placa
       
        
        for item in data_placa:
            canal           =   item['canal_placa']#pega canal 
            id_sensor       =   item['sensor_placa']#pega o sensor
            chave_cordoes.append(item['cordao_fisico'])#pego nomes dos cordoes fisicos

            if canal not in resultado_agrupado:
                resultado_agrupado[canal] = [id_sensor]#cria o dicionario , caso a chave 'canal" ainda não exista , caso contrario ele apenas adiciona o sensor a lista na linha 97
            else:
                resultado_agrupado[canal].append(id_sensor)

        lista_final     =   [{canal:sensores} for canal , sensores in resultado_agrupado.items()]#cria lista de dicionario [{1:[1,2,3,4,5]},{2:[1,2,3,4,5]},{3:[1,2,3,4,5]}] a api espera essa estrutura
        print(lista_final)
        for ip in ip_placa:
            url = f'http://{ip}/api/teste/'
            response = requests.post(url, json=lista_final)

            if response.status_code == 200:
                response_content = response.text
                print('Conteúdo da resposta:', response_content)
            else:
                print('Ocorreu um erro ao fazer a solicitação POST:', response.text)


if __name__ == '__main__':

    app = App()
    app.exe_read_temp()
    app.read_temp_placa_secun()
