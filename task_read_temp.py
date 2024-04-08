import json
from datetime import date
from datetime import datetime
import threading
from manager_placa import ManagerPlacaSlave
from factory import  FactoryPlacaSlave


class ManagerObjectPlacaSlave(ManagerPlacaSlave):

    _list_placa = []

    def create_object(self):    
        
        for obj in self._cod_placa:
            obj_str = str(obj)
            _factory_placa = FactoryPlacaSlave()
            name = 'Placa' + f'{obj_str}'
            placa = _factory_placa.create_placa(name)
            self._list_placa.append(placa)




    def save(self, data):
        self.registro_instal.registros_temperaturas     =   json.dumps(data)
        self.registro_instal.data                       =   self.dt.now()
        self.conn.insert_registro_instalacao(self.registro_instal)

class ManagerThreads(ManagerObjectPlacaSlave):


    def _init_threds(self):
        self.create_object()
        tasks = []


        for placa in self._list_placa:
            th = threading.Thread(target=placa.read_temp())

            tasks.append(th)

        [th.start() for th in tasks]

        [th.join() for th in tasks]


class App:

    def run(self):

        threads = ManagerThreads()
        threads._init_threds()


if __name__ == "__main__":

    app = App()
    app.run()



 