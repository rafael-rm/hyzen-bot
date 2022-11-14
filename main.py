import discord
import os
import asyncio
import dotenv
from discord.ext import commands


dotenv.load_dotenv()
token = os.getenv('TOKEN')


class App(commands.Bot):
    def __init__(self):
        super().__init__(
            intents = discord.Intents.default(),
            command_prefix = '.'
        )

    async def load(self):
        for folder in os.listdir('./src'):
            for folder2 in os.listdir(f'./src/{folder}'):
                for file in os.listdir(f'./src/{folder}/{folder2}'):
                    if file.endswith('.py'):
                        await self.load_extension(f'src.{folder}.{folder2}.{file[:-3]}')
                        print(f'[INFO] Encontrado arquivo: {file[:-3]}')


    async def main(self):
        await App.load(self)
        await self.start(token)


asyncio.run(App().main())