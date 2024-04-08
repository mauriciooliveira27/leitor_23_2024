import json
from datetime import datetime
from model import registro_instalacao
import threading
from model import Db_information
import data_base



class ManagerPlacaSlave:

    _cod_placa  =   []
    _ip_placa   =   []

    def __init__(self) -> None:
            self.db                         =       Db_information("Termometria",3306,"localhost","leitor_termo","termometria")
            self.conn                       =       data_base.Connector(self.db)
            self.conf                       =       self.conn.get_informaton_instal()
            self.data_instal                =       json.loads(self.conf.dados)
            self.dt                         =       datetime
            self.read_temp                  =       True
            self.registro_instal            =       registro_instalacao(0, self.conf.nome, self.conf.configuracao_fisica, self.dt.now(), "")
            self.result_placa_slave         =       None
            self.lock                       =       threading.RLock()
            self.execute()
    

    def execute(self):
        with self.lock:
            self.result_placa_secund    =       self.conn.select_placa_secund()
        cod_placa       =   [cod['cod_placa'] for cod in self.result_placa_secund]
        ip_placa        =   [ip['ip'] for ip in self.result_placa_secund]

        self._cod_placa =   cod_placa
        self._ip_placa  =   ip_placa