import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db
import os
import dotenv
import configparser


dotenv.load_dotenv()
database_url = str(os.getenv('DATABASE_URL'))

config = configparser.ConfigParser()
config.read('config.conf')
numero_comandos_atualizar_db = int(config['DATABASE']['NUM_COMANDOS_ATUALIZAR_DB'])


class FirebaseDB():
    def __init__(self):
        cred = credentials.Certificate("./serviceAccountKey.json")
        firebase_admin.initialize_app(cred, {'databaseURL': database_url})
        self.db = firestore.client()
        self.contador_cmds = 0


    async def contador_comandos(self):
        self.contador_cmds += 1
        if self.contador_cmds == numero_comandos_atualizar_db:
            self.contador_cmds = 0
            request = db.reference('/global')
            if request.get() is None:
                request.set({
                    'comandos-executados': numero_comandos_atualizar_db
                })
            else:
                request.update({
                    'comandos-executados': request.get()['comandos-executados'] + numero_comandos_atualizar_db
                })