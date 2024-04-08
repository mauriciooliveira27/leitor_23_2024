import json
from datetime import date
from datetime import datetime
import threading
from manager_placa import ManagerPlacaSlave
from factory import  FactoryPlacaSlave


class ManagerObjectPlacaSlave(ManagerPlacaSlave):

    _list_placa = []    


    def create_object(self):    
        self.cod = self._cod_placa
        self.ip = self._ip_placa

        for indice , obj in  enumerate(self._cod_placa):
            _factory_placa = FactoryPlacaSlave()
            ip = self.ip[indice]

            placa = _factory_placa.create_placa(ip, obj)
            self._list_placa.append(placa)

    def save(self, data):
        self.registro_instal.registros_temperaturas     =   json.dumps(data)
        self.registro_instal.data                       =   self.dt.now()
        self.conn.insert_registro_instalacao(self.registro_instal)

    
    @property
    def get_list(self):
        return self._list_placa


class ManagerThreads(ManagerObjectPlacaSlave):


    def _init_threds(self):
        self.create_object()
        tasks = []
        print(self.ip)
        print(self.cod)
        print('teste')

        for placa in self._list_placa:
            th = threading.Thread(target=placa.read_temp)

            tasks.append(th)

        [th.start() for th in tasks]

        [th.join() for th in tasks]

    
        placas = self.get_list
        json = {}
        for pl in placas:
            json.update(pl.result_placa_secund)

        print(json)

class App:

    def run(self):

        threads = ManagerThreads()
        threads._init_threds()


if __name__ == "__main__":

    app = App()
    app.run()



 