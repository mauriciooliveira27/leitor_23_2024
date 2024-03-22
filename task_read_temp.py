import data_base
from model import Db_information
import json
from leitor_termo import Leitor_temp
from multiplex import Multiplex3
import time
from datetime import date
from datetime import datetime
from model import registro_instalacao


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

            data = self.conn.select_placa_main()
            resultado_agrupado = {}
            chave_cordoes = []

            for item in data:
                canal       =       item['canal_placa']
                id_sensor   =       item['sensor_placa']
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
                        leituras.append(value_sensor)

              
            print(chave_cordoes)
            print(leituras)
            resultado = dict(zip(chave_cordoes, leituras))
            #form record
            #record = Registro(conf, datetime.now().strftime("%d/%m/%Y"),str(datetime.time(datetime.now())), json.dumps(data_temp))
            #conn.insert_record(record)
            self.registro_instal.registros_temperaturas = json.dumps(resultado)
            self.registro_instal.data = self.dt.now()
            self.conn.insert_registro_instalacao(self.registro_instal)



if __name__ == '__main__':

    app = App()

    app.exe_read_temp()
