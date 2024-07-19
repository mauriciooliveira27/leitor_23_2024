import http.client 
import json
from .query import Formatador
from .query_database import *
import time
from .database import MysqlConnection
from datetime import datetime
from .update_revenue import validar

class ResponseApi:
 
    def treat_response(self, response):
        global response_api
        content_type            =       response.headers.get('Content-Type', '')

        if 'application/json' in content_type:
            response_json       =       json.loads(response.read().decode('utf-8'))
            response_api        =       response_json
            result              =       validar(response_api,dados_enviar,dados_receita)

            if result == True:
                #print("web mais atual , atualiando embarcado")
                time.sleep(5)
                #print("embarcado atualizado.")
                content = response.read()
                return True
            
            if result == False:
                #print("embarcado mais atual")
                return False
            
            if result == "integrações atualizadas":
                #print("EMBARCADO E WEB ESTÃO SINCRONIZADOS COM A MESTA RECEITA REFERENTE A DATA/HORA")
                return True
            #print(content)
        
           
        if response.status == 500:
            # time.sleep(30)
            #print("Erro 500 encontrado . Obtendo o conteúdo do erro...")
            content = response.read()
            #print(content)
            db = MysqlConnection()
            db.set_query(error_status500())
            
            return content_type
        elif response.status == 404:
            # time.sleep(30)
            db = MysqlConnection()
            db.set_query(error_status404())
            #print("Erro 404: recurso não encontrado . Verifique se a URL ou a rota está corre.")
            
            return content_type