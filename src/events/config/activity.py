from discord.ext import commands
import dotenv
import os
import discord
from datetime import timezone

class Activity(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[INFO] Carregado arquivo: {__name__}')
        await self.bot.change_presence(activity=discord.Game(name="hyzen.com.br"))


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Activity(bot))