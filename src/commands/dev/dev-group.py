import discord
from discord import app_commands
from discord.ext import commands
from src.database.firebase import FirebaseDB
import psutil
import configparser
from datetime import timezone


class DevCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    group = app_commands.Group(name="dev", description="Comandos de desenvolvedor.")


    def permissao_usar_cmd():
        def predicate(interaction: discord.Interaction) -> bool:
            config = configparser.ConfigParser()
            config.read("config.ini")
            return interaction.user.id == config.getint("IDS", "DESENVOLVEDOR")
        return app_commands.check(predicate)


    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[INFO] Carregado arquivo: {__name__}')


    # Comando de TESTE
    @group.command(name='teste', description='Teste de comando.')
    @permissao_usar_cmd()
    async def teste(self, interaction: discord.Interaction):
        await FirebaseDB.contador_comandos(self.bot.database)
        await interaction.response.send_message('Teste de comando.')


    # Comando de PING
    @group.command(name='ping', description='Mostra o ping da aplicação.')
    @permissao_usar_cmd()
    async def ping(self, interaction: discord.Interaction): 
        await FirebaseDB.contador_comandos(self.bot.database)
        await interaction.response.send_message(f"A aplicação encontra-se com **{round(self.bot.latency * 1000)}ms** de latência") 


    # Comando de RAM
    @group.command(name='ram', description='Mostra o uso de RAM do servidor.')
    @permissao_usar_cmd()
    async def ram(self, interaction: discord.Interaction):
        await FirebaseDB.contador_comandos(self.bot.database)
        await interaction.response.send_message(f"A máquina encontra-se utilizando **{psutil.virtual_memory().used / 1024 / 1024:.0f}/{psutil.virtual_memory().total / 1024 / 1024:.0f}MB ({psutil.virtual_memory().percent}%)** de RAM")


    # Comando de CPU
    @group.command(name='cpu', description='Mostra o uso da CPU do servidor.')
    @permissao_usar_cmd()
    async def cpu(self, interaction: discord.Interaction):
        await FirebaseDB.contador_comandos(self.bot.database)
        await interaction.response.send_message(f"A máquina possui **{psutil.cpu_count()} núcleos lógicos** e está utilizando **{psutil.cpu_percent()}%** de sua capacidade total")

    
    # Comando de SYNC
    @group.command(name='sync', description='Sincroniza os comandos da aplicação.')
    @permissao_usar_cmd()
    async def sync(self, interaction: discord.Interaction):
        await FirebaseDB.contador_comandos(self.bot.database)
        await interaction.response.send_message('Sincronizando aplicação com o Discord...')
        await self.bot.tree.sync()
        await interaction.channel.send('Aplicação sincronizada com o Discord.')


    # Comando de SHARD
    @group.command(name='shard', description='Mostra informações sobre os shards.')
    @permissao_usar_cmd()
    async def shard(self, interaction: discord.Interaction):
        if interaction.guild is not None:
            await FirebaseDB.contador_comandos(self.bot.database)
            mensagem = f"A aplicação possui **{self.bot.shard_count} shards.** \nShard atual: **{interaction.guild.shard_id}** \nPing médio: **{round(self.bot.latency * 1000)}ms**```"
            for shard in self.bot.latencies:
                mensagem += f"\nShard {shard[0]}: {round(shard[1] * 1000)}ms"
            mensagem += "```"
            await interaction.response.send_message(mensagem)
        else:
            mensagem = f"A aplicação possui **{self.bot.shard_count} shards.** \nShard atual: **0** \nPing médio: **{round(self.bot.latency * 1000)}ms**```"
            for shard in self.bot.latencies:
                mensagem += f"\nShard {shard[0]}: {round(shard[1] * 1000)}ms"
            mensagem = mensagem + "```"
            await interaction.response.send_message(f"{mensagem}")


    # Erro do comando TESTE
    @teste.error
    async def teste_error(self, interaction: discord.Interaction, error):
        await FirebaseDB.contador_comandos(self.bot.database)
        if isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message("Você não tem permissão para executar esse comando.", ephemeral=True)
        else:
            await interaction.response.send_message("Ocorreu um erro ao executar o comando.", ephemeral=True)
            print(error)


    # Erro do comando PING
    @ping.error
    async def ping_error(self, interaction: discord.Interaction, error):
        await FirebaseDB.contador_comandos(self.bot.database)
        if isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message("Você não tem permissão para executar esse comando.", ephemeral=True)
        else:
            await interaction.response.send_message("Ocorreu um erro ao executar o comando.", ephemeral=True)
            print(error)


    # Erro do comando RAM
    @ram.error
    async def ram_error(self, interaction: discord.Interaction, error):
        await FirebaseDB.contador_comandos(self.bot.database)
        if isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message("Você não tem permissão para executar esse comando.", ephemeral=True)
        else:
            await interaction.response.send_message("Ocorreu um erro ao executar o comando.", ephemeral=True)
            print(error)


    # Erro do comando CPU
    @cpu.error
    async def cpu_error(self, interaction: discord.Interaction, error):
        await FirebaseDB.contador_comandos(self.bot.database)
        if isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message("Você não tem permissão para executar esse comando.", ephemeral=True)
        else:
            await interaction.response.send_message("Ocorreu um erro ao executar o comando.", ephemeral=True)
            print(error)


    # Erro do comando SYNC
    @sync.error
    async def sync_error(self, interaction: discord.Interaction, error):
        await FirebaseDB.contador_comandos(self.bot.database)
        if isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message("Você não tem permissão para executar esse comando.", ephemeral=True)
        else:
            await interaction.response.send_message("Ocorreu um erro ao executar o comando.", ephemeral=True)
            print(error)

        
    # Erro do comando SHARD
    @shard.error
    async def shard_error(self, interaction: discord.Interaction, error):
        await FirebaseDB.contador_comandos(self.bot.database)
        if isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message("Você não tem permissão para executar esse comando.", ephemeral=True)
        else:
            await interaction.response.send_message("Ocorreu um erro ao executar o comando.", ephemeral=True)
            print(error)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(DevCommands(bot))