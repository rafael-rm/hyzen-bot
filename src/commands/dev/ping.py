import discord
from discord import app_commands
from discord.ext import commands


class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[INFO] Carregado arquivo: {__name__}')


    @app_commands.command(name='ping', description='Latência da aplicação.')
    async def ping(self, interaction: discord.Interaction): 
        await interaction.response.send_message(f"A aplicação encontra-se com **{round(self.bot.latency * 1000)}ms** de latência") 

    
    @ping.error
    async def ping_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message("Ocorreu um erro ao executar o comando.", ephemeral=True)
        


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Ping(bot))
