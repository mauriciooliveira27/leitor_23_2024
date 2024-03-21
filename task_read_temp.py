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
      

        data = conn.select_placa_main()

        resultado_agrupado = {}
        # Agrupando os dados pelo canal_placa

        for item in data:
            canal = item['canal_placa']
            id_sensor = item['sensor_placa']
            if canal not in resultado_agrupado:
                resultado_agrupado[canal] = [id_sensor]
            else:
                resultado_agrupado[canal].append(id_sensor)
        # Convertendo o dicionário para a lista desejada
                

        lista_final = [{canal: sensores} for canal, sensores in resultado_agrupado.items()]


        data_temp.clear()
        result  =   {}
        print(lista_final)

        for canal in lista_final:
            canals           =       canal.keys()
            sensores        =       list(canal.values())
            sensores_list   =       sensores[0]
      
                #Set hardware channel and sensor
            for c in canal:
           
                for s in sensores_list:
                    chave           =       'Ch' + str(c) + 'S' + str(s)
                 
                    c_int           =       int(c)
                    s_int           =       int(s)
                    mp.set_canal(c_int)
                    mp.set_sensor(s_int)
                    value_sensor = leitor.read_temp()
                    result[chave]   =       f'{value_sensor:.2f}'


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
                    record_sensor.valor = result
                    conn.insert_record_sensor(record_sensor)
            #form record
            #record = Registro(conf, datetime.now().strftime("%d/%m/%Y"),str(datetime.time(datetime.now())), json.dumps(data_temp))
            #conn.insert_record(record)
            registro_instal.registros_temperaturas = json.dumps(result)
            registro_instal.data = dt.now()
            conn.insert_registro_instalacao(registro_instal)
            read_temp = False

