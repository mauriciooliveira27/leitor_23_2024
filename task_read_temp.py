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
import threading
class App:
        
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
        self.reult_placa_main       =       None
        self.result_placa_secund    =       None
        self.lock                   =       threading.RLock()


    def exe_read_temp(self):
        print('PLACA MAIN')
        with self.lock:
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
                    time.sleep(0.3)
                    leituras.append(f'{value_sensor:.2f}')

        resultado      =   dict(zip(chave_cordoes, leituras))
        self.reult_placa_main =  resultado


    def get_data_placa(self):
       
        result          =   self.conn.select_placa_secund() 
        cod_placa       =   [cod['cod_placa'] for cod in result]
        ip_placa        =   [ip['ip'] for ip in result]
        return cod_placa  , ip_placa
    


    def read_temp_placa_secun(self):
        print('PLACA SECUNDARIA')
        with self.lock:
            cod_placa,ip_placa      =   self.get_data_placa()
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
            while erro < 3:
                try:
                    url                 =   f'http://{ip}/api/get_temp/'
                    response            =   requests.post(url, json=lista_final)   
                    leituras            =   response.text
                    status_cod          =   response.status_code
                    print(status_cod)

                    if status_cod == 200:
                        leitura_list        =   json.loads(leituras)
                        response_content    =   dict(zip(chave_cordoes,leitura_list))
                        chave_cordoes.clear()
                        data_temp.update(response_content)
                        self.result_placa_secund = data_temp
                        break

                except requests.exceptions.RequestException as e:
                    time.sleep(30)
                    erro += 1
                    print('Erro de requisição:', e)
                    print('dentro do except')
                    print(erro)

                except Exception as e:
                    time.sleep(30)
                    erro += 1
                    print('Erro:', e)
                    print('dentro do except')
                    print(erro)

                if erro == 3:
                    self.result_placa_secund = {chave: '' for chave in chave_cordoes }
                    break


    def save(self, data):
        self.registro_instal.registros_temperaturas     =   json.dumps(data)
        self.registro_instal.data                       =   self.dt.now()
        self.conn.insert_registro_instalacao(self.registro_instal)


def main():
    app = App()
    th1 = threading.Thread(target=app.exe_read_temp)
    th2 = threading.Thread(target=app.read_temp_placa_secun)

    th1.start()
    th2.start()

    th1.join()
    th2.join()

    JSON1 = app.reult_placa_main
    JSON2 = app.result_placa_secund

    if JSON2 != None:
        JSON_COMPLETE   =   {**JSON1, **JSON2}
        app.save(JSON_COMPLETE)
        return
    elif JSON2 == None:
        app.save(JSON1)
        return


if __name__ == '__main__':
    dt = datetime
    if dt.now().minute == 0 and dt.now().second < 20:
        main()