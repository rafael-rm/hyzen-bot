import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db
import os
import dotenv


NUM_COMANDOS_ATUALIZAR_DB = 10


dotenv.load_dotenv()
database_url = str(os.getenv('DATABASE_URL'))


class FirebaseDB():
    def __init__(self):
        cred = credentials.Certificate("./serviceAccountKey.json")
        firebase_admin.initialize_app(cred, {'databaseURL': database_url})
        self.db = firestore.client()
        self.contador_cmds = 0


    async def contador_comandos(self):
        self.contador_cmds += 1
        if self.contador_cmds == NUM_COMANDOS_ATUALIZAR_DB:
            self.contador_cmds = 0
            request = db.reference('/global')
            if request.get() is None:
                request.set({
                    'comandos-executados': NUM_COMANDOS_ATUALIZAR_DB
                })
            else:
                request.update({
                    'comandos-executados': request.get()['comandos-executados'] + NUM_COMANDOS_ATUALIZAR_DB
                })