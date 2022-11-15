import discord
import os
import asyncio
import dotenv
from discord.ext import commands
from src.database.firebase import FirebaseDB


dotenv.load_dotenv()
token = os.getenv('TOKEN')


class App(commands.Bot):
    def __init__(self):
        super().__init__(
            intents = discord.Intents.default(),
            command_prefix = '.'
        )
        self.database = FirebaseDB()


    async def load(self):
        for folder in os.listdir('./src/commands'):
            for file in os.listdir(f'./src/commands/{folder}'):
                if file.endswith('.py'):
                    try:
                        print(f'[INFO] Encontrado arquivo: {file}')
                        await self.load_extension(f'src.commands.{folder}.{file[:-3]}')
                    except Exception as error:
                        print(f'[ERRO] - {error}')

        for file in os.listdir('./src/events'):
            if file.endswith('.py'):
                try:
                    print(f'[INFO] Encontrado arquivo: {file}')
                    await self.load_extension(f'src.events.{file[:-3]}')
                except Exception as error:
                    print(f'[ERRO] - {error}')


    async def main(self):
        await App.load(self)
        await self.start(token)


asyncio.run(App().main())