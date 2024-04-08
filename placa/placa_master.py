import time
from .placa_abs import PlacaAbstract
from multiplex import Multiplex3
from typing import Type
from manager_placa import ManagerPlacaMaster
from leitor_termo import Leitor_temp


class PlacaMaster(PlacaAbstract,Multiplex3):

    leituras        =       []


    def __init__(self) -> None:
        self.leitor                 =       Leitor_temp()
        self.result_placa_master    =       None


    def read_temp(self, placa : Type[ManagerPlacaMaster] ):

        placa.execute()
        for canal in placa.lista_CodSen:
            canals              =       canal.keys()
            sensores            =       list(canal.values())
            sensores_list       =       sensores[0]
    
            #Set hardware channel and sensor
            for c in canal:
        
                for s in sensores_list:
                
                    c_int           =       int(c)
                    s_int           =       int(s)
                    self.set_canal(c_int)
                    self.set_sensor(s_int)
                    value_sensor    =       self.leitor.read_temp()
                    time.sleep(1)
                    self.leituras.append(f'{value_sensor:.2f}')

        resultado               =   dict(zip(placa.chave_cordoes, self.leituras))
        self.result_placa_master =   resultado

