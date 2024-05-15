import json
from datetime import date
from datetime import datetime
import threading
from core.manager_placa import ManagerPlacaSlave
from core.factory.factory_placa_master import  FactoryPlacaMaster
from core.factory.factory_placa_slave import  FactoryPlacaSlave
import time

class App:
    placa = FactoryPlacaMaster()
    placa_master = placa.create_placa()

    @classmethod
    def run(cls):
        cls.placa_master.read_temp()
        leitura = cls.placa_master.result_placa_master
        cls.placa_master.save(leitura)


if __name__ ==  '__main__':
    dt = datetime
    
    if dt.now().minute == 0 and dt.now().second < 30:
        App.run()
        time.sleep(5)