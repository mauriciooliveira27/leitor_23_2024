import time
from .placa_abs import PlacaAbstract
from .multiplex import Multiplex3
from typing import Type
from manager_placa import ManagerPlacaMaster
from leitor_termo import Leitor_temp
import json


class PlacaMaster(PlacaAbstract,ManagerPlacaMaster):

    leituras        =       []
    mp              =       Multiplex3

    def __init__(self) -> None:
        self.leitor                 =       Leitor_temp()
        self.result_placa_master    =       None
        


    def read_temp(self):

        self.execute()
        for canal in self.lista_CodSen:
            print(canal)
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
                    time.sleep(1)
                    self.leituras.append(f'{value_sensor:.2f}')

        resultado               =   dict(zip(self.chave_cordoes, self.leituras))
        self.result_placa_master =   resultado

    def save(self, data):
        self.registro_instal.registros_temperaturas     =   json.dumps(data)
        self.registro_instal.data                       =   self.dt.now()
        self.conn.insert_registro_instalacao(self.registro_instal)