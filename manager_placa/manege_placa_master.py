from model import Db_information
import json
from datetime import datetime
from model import registro_instalacao
import threading
import data_base


class ManagerPlacaMaster:

        lista_CodSen                    =       []
        chave_cordoes                   =       []

        def __init__(self) -> None:
                self.db                     =       Db_information("Termometria",3306,"localhost","leitor_termo","termometria")
                self.conn                   =       data_base.Connector(self.db)
                self.conf                   =       self.conn.get_informaton_instal()
                self.data_instal            =       json.loads(self.conf.dados)
                self.dt                     =       datetime
                self.read_temp              =       True
                self.registro_instal        =       registro_instalacao(0, self.conf.nome, self.conf.configuracao_fisica, self.dt.now(), "")
                self.reult_placa_master       =       None
                self.lock                   =       threading.RLock()
                self.execute()
        
        def execute(self):
                with self.lock:
                        data_placa                      =       self.conn.select_placa_main()
                resultado_agrupado              =       {}
                

                for item in data_placa:

                        self.canal               =       item['canal_placa']
                        self.id_sensor           =       item['sensor_placa']
                        self.chave_cordoes.append(item['cordao_fisico'])

                        if self.canal not in resultado_agrupado:
                                resultado_agrupado[self.canal] = [self.id_sensor]
                        else:
                                resultado_agrupado[self.canal].append(self.id_sensor)

                # Convertendo o dicionário para a lista desejada
                self.lista_CodSen     =       [{canal: sensores} for canal, sensores in resultado_agrupado.items()]
                