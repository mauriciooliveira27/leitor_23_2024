import data_base
from model import Db_information

db = Db_information("Termometria",3306,"localhost","leitor_termo","termometria")
conn = data_base.Connector(db)

data = conn.select_placa_secun()
print(data)