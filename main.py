import discord
import os
import asyncio
import dotenv
from discord.ext import commands
import datetime
import logging
import src.functions.logs as logs
from src.database.firebase import FirebaseDB


logs.main()

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
        self.time_start = datetime.datetime.now().timestamp()
        self.firebase = FirebaseDB()
        self.cache_comandos_executados = 0


    async def load(self):
        for file in os.listdir(f'./src/commands/'):
            if file.endswith('.py'):
                try:
                    logging.info(f'Encontrado arquivo: {file}')
                    await self.load_extension(f'src.commands.{file[:-3]}')
                except Exception as error:
                    logging.error(f'{error}')

        for file in os.listdir(f'./src/events/'):
            if file.endswith('.py'):
                try:
                    logging.info(f'Encontrado arquivo: {file}')
                    await self.load_extension(f'src.events.{file[:-3]}')
                except Exception as error:
                    logging.error(f'{error}')


    async def main(self):
        await App.load(self)
        await self.start(token_prod)


asyncio.run(App().main())