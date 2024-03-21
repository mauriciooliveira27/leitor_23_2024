#Modules
#Data Base
import model
import data_base
from model import Db_information
from model import Config_install
from model import Registro
from model import Registro_sensor
from model import registro_instalacao
import json
import requests



#Hardware
from leitor_termo import Leitor_temp
from multiplex import Multiplex3

#date time
import time
from datetime import date
from datetime import datetime

#Read configuration installation
db = Db_information("Termometria",3306,"localhost","leitor_termo","termometria")
conn = data_base.Connector(db)
conf = conn.get_informaton_instal()
data_instal = json.loads(conf.dados)

canais = data_instal["Cordoes"]
sensores = []
for key in data_instal.keys():
    sensores.append(data_instal[key])
sensores.pop(0)

#initialization hardware
leitor = Leitor_temp()
mp = Multiplex3()

#bool var start reading
enable_read_loop = True
read_temp = True
key = ""
key_sensor = ""
value = ""
dt = datetime
value_sensor = 0.0

#Registro
data_temp = {}
record_sensor = Registro_sensor(dt.now(), dt.now(), "", 1, 0.0)
registro_instal = registro_instalacao(0, conf.nome, conf.configuracao_fisica, dt.now(), "")

while(enable_read_loop):
    time.sleep(1.0)
    if (dt.now().minute == 0 and dt.now().second < 5 and read_temp == False):
        read_temp = True

    if(read_temp):

        data = conn.select_estacao_mt()
        print(data)


        data_temp.clear()
        for canal in range(canais):
            for sensor in range(sensores[canal]):
                #Set hardware channel and sensor
                mp.set_canal(canal+1)
                mp.set_sensor(sensor+1)
                time.sleep(1.0)
                #crete key label data
                key = str(f"Ch{canal+1}S{sensor+1}")
                key_sensor = str(f"CL3/SL18/CO{canal+1}/S{sensor+1}")
                value_sensor = leitor.read_temp()
                value = "{:.2f}".format(value_sensor)

                time.sleep(0.3)

                #one_register = {key:value}
                #data_temp.update(one_register)
                if key not in data_temp.keys():
                    data_temp[key] = value
                #print(data_temp)

                #record sensor
                record_sensor.created_at = dt.now()
                record_sensor.data_hora = dt.now()
                record_sensor.tag = key_sensor
                record_sensor.tipo = 1
                record_sensor.valor = value_sensor
                conn.insert_record_sensor(record_sensor)
        #form record
        #record = Registro(conf, datetime.now().strftime("%d/%m/%Y"),str(datetime.time(datetime.now())), json.dumps(data_temp))
        #conn.insert_record(record)
        registro_instal.registros_temperaturas = json.dumps(data_temp)
        registro_instal.data = dt.now()
        conn.insert_registro_instalacao(registro_instal)
        read_temp = False

