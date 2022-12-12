import discord
import os
import asyncio
import dotenv
from discord.ext import commands
from src.database.firebase import FirebaseDB
import datetime


client_intents = discord.Intents.default()
client_intents.members = True


dotenv.load_dotenv()
token_canary = os.getenv('TOKEN-CANARY')
token_prod = os.getenv('TOKEN-PROD')


class App(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(
            intents = client_intents,
            command_prefix = '.',
            shard_count = 1,
        )
        self.database = FirebaseDB()
        self.time_start = datetime.datetime.now().timestamp()


    async def load(self):
        for folder in os.listdir('./src/commands'):
            for file in os.listdir(f'./src/commands/{folder}'):
                if file.endswith('.py'):
                    try:
                        print(f'[INFO] Encontrado arquivo: {file}')
                        await self.load_extension(f'src.commands.{folder}.{file[:-3]}')
                    except Exception as error:
                        print(f'[ERRO] {error}')

        for folder in os.listdir('./src/events'):
            for file in os.listdir(f'./src/events/{folder}'):
                if file.endswith('.py'):
                    try:
                        print(f'[INFO] Encontrado arquivo: {file}')
                        await self.load_extension(f'src.events.{folder}.{file[:-3]}')
                    except Exception as error:
                        print(f'[ERRO] {error}')


    async def main(self):
        await App.load(self)
        await self.start(token_canary)


asyncio.run(App().main())