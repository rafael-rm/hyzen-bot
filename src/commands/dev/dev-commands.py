import discord
from discord import app_commands
from discord.ext import commands
from src.database.firebase import FirebaseDB
import psutil

class Dev(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    group = app_commands.Group(name="dev", description="Comandos de desenvolvimento")


    def permissao_usar_cmd():
        def predicate(interaction: discord.Interaction) -> bool:
            return interaction.user.id == 383756503989092353
        return app_commands.check(predicate)


    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[INFO] Carregado arquivo: {__name__}')


    @group.command(name='ping', description='Mostra o ping da aplicação.')
    @permissao_usar_cmd()
    async def ping(self, interaction: discord.Interaction): 
        await FirebaseDB.contador_comandos(self.bot.database)
        await interaction.response.send_message(f"A aplicação encontra-se com **{round(self.bot.latency * 1000)}ms** de latência") 

    
    @group.command(name='ram', description='Mostra o uso de RAM do servidor.')
    @permissao_usar_cmd()
    async def ram(self, interaction: discord.Interaction):
        await FirebaseDB.contador_comandos(self.bot.database)
        await interaction.response.send_message(f"A máquina encontra-se utilizando **{psutil.virtual_memory().used / 1024 / 1024:.0f}/{psutil.virtual_memory().total / 1024 / 1024:.0f}MB** de memória RAM")


    @group.command(name='cpu', description='Mostra o uso da CPU do servidor.')
    @permissao_usar_cmd()
    async def cpu(self, interaction: discord.Interaction):
        await FirebaseDB.contador_comandos(self.bot.database)
        await interaction.response.send_message(f"A máquina encontra-se utilizando **{psutil.cpu_percent()}%** de CPU")

    
    @ping.error
    async def ping_error(self, interaction: discord.Interaction, error):
        await FirebaseDB.contador_comandos(self.bot.database)
        if isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message("Você não tem permissão para executar esse comando.", ephemeral=True)
        else:
            await interaction.response.send_message("Ocorreu um erro ao executar o comando.", ephemeral=True)
            print(error)


    @ram.error
    async def ram_error(self, interaction: discord.Interaction, error):
        await FirebaseDB.contador_comandos(self.bot.database)
        if isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message("Você não tem permissão para executar esse comando.", ephemeral=True)
        else:
            await interaction.response.send_message("Ocorreu um erro ao executar o comando.", ephemeral=True)
            print(error)


    @cpu.error
    async def cpu_error(self, interaction: discord.Interaction, error):
        await FirebaseDB.contador_comandos(self.bot.database)
        if isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message("Você não tem permissão para executar esse comando.", ephemeral=True)
        else:
            await interaction.response.send_message("Ocorreu um erro ao executar o comando.", ephemeral=True)
            print(error)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Dev(bot))