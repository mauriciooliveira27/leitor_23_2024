import json
from datetime import date
from datetime import datetime
import threading
from manager_placa import ManagerPlacaSlave
from factory import  FactoryPlacaSlave


class ManagerObjectPlacaSlave(ManagerPlacaSlave):

    _list_placa = []
    _factory_placa = FactoryPlacaSlave()

    def create_object(self):
        
        for obj in self._cod_placa:
            obj_str = str(obj)
            name = 'Placa' + f'{obj_str}'
            placa = self._factory_placa.create_placa(name)
            print(placa)
            self._list_placa.append(placa)




# def save(self, data):
#     self.registro_instal.registros_temperaturas     =   json.dumps(data)
#     self.registro_instal.data                       =   self.dt.now()
#     self.conn.insert_registro_instalacao(self.registro_instal)


# def main():
#     app = App()
#     th1 = threading.Thread(target=app.exe_read_temp)
#     th2 = threading.Thread(target=app.read_temp_placa_secun)

#     th1.start()
#     th2.start()

#     th1.join()
#     th2.join()

#     JSON1 = app.reult_placa_main
#     JSON2 = app.result_placa_secund

#     if JSON2 != None:
#         JSON_COMPLETE   =   {**JSON1, **JSON2}
#         app.save(JSON_COMPLETE)
#         return
#     elif JSON2 == None:
#         app.save(JSON1)
#         return


# if __name__ == '__main__':
    
#     dt = datetime
#     if dt.now().minute == 0 and dt.now().second < 5:
#         main()