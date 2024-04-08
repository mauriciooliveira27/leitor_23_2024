import time
from .placa_abs import PlacaAbstract
from .multiplex import Multiplex3
from typing import Type
from manager_placa import ManagerPlacaMaster

import json


class PlacaMaster(PlacaAbstract,ManagerPlacaMaster):

    leituras        =       []
    mp              =       Multiplex3()

    def __str__(self) -> str:
        return 'Iniciando leitura Placa-Master'
    
    def read_temp(self):
        for canal in self.lista_CodSen:
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
                    time.sleep(1)
                    self.leituras.append(f'{value_sensor:.2f}')

        resultado               =   dict(zip(self.chave_cordoes, self.leituras))
        self.result_placa_master =   resultado

    def save(self, data):
        self.registro_instal.registros_temperaturas     =   json.dumps(data)
        self.registro_instal.data                       =   self.dt.now()
        self.conn.insert_registro_instalacao(self.registro_instal)