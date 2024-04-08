import json
from datetime import date
from datetime import datetime
import threading
from manager_placa import ManagerPlacaSlave
from factory import  FactoryPlacaSlave, FactoryPlacaMaster


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

        factory_master = FactoryPlacaMaster()
        placa_master = factory_master.create_placa()

        th_master = threading.Thread(target=placa_master.read_temp)

        for placa in self._list_placa:
            th = threading.Thread(target=placa.read_temp)

            tasks.append(th)

        th_master.start()
        

        [th.start() for th in tasks]

        [th.join() for th in tasks]
        th_master.join()
    
        placas = self.get_list
        json_master = placa_master.result_placa_master
        json_slaves = {}

        for pl in placas:
            json_slaves.update(pl.result_placa_secund)

        json_complete = {**json_slaves , **json_master}
        print(json_complete)


class App:

    def run(self):

        threads = ManagerThreads()
        threads._init_threds()


if __name__ == "__main__":

    app = App()
    app.run()



 