import json
from datetime import date
from datetime import datetime
import threading
from manager_placa import ManagerPlacaSlave
from factory.factory_placa_master import  FactoryPlacaMaster
from factory.factory_placa_slave import  FactoryPlacaSlave
import time

class App:

    placa = FactoryPlacaMaster()
    placa_master = placa.create_placa()

    @classmethod
    def run(cls):
        cls.placa_master.read_temp()


if __name__ ==  '__main__':

    dt = datetime
    if dt.now().minute == 0 and dt.now().second < 30:
        App.run()
        time.sleep(5)