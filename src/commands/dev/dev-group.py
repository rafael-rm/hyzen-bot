import discord
from discord import app_commands
from discord.ext import commands
from src.others.comando_executado import comando_executado
import psutil
import datetime
import configparser
import logging
import os

class DevCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    group = app_commands.Group(name="dev", description="Comandos de desenvolvedor.")


    def permissao_usar_cmd():
        def predicate(interaction: discord.Interaction) -> bool:
            config = configparser.ConfigParser()
            config.read('config.conf')
            desenvolvedor_id = int(config['IDS']['DESENVOLVEDOR_ID'])
            return interaction.user.id == desenvolvedor_id
        return app_commands.check(predicate)


    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Carregado: {__name__}')


    # Comando de PING
    @group.command(name='ping', description='Mostra o ping da aplicação.')
    @permissao_usar_cmd()
    async def ping(self, interaction: discord.Interaction): 
        await interaction.response.send_message(f"A aplicação encontra-se com **{round(self.bot.latency * 1000)}ms** de latência") 
        await comando_executado(interaction, self.bot)


    # Comando de RAM
    @group.command(name='ram', description='Mostra o uso de RAM do servidor.')
    @permissao_usar_cmd()
    async def ram(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"A máquina encontra-se utilizando **{psutil.virtual_memory().used / 1024 / 1024:.0f}/{psutil.virtual_memory().total / 1024 / 1024:.0f}MB ({psutil.virtual_memory().percent}%)** de RAM")
        await comando_executado(interaction, self.bot)


    # Comando de CPU
    @group.command(name='cpu', description='Mostra o uso da CPU do servidor.')
    @permissao_usar_cmd()
    async def cpu(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"A máquina possui **{psutil.cpu_count()} núcleos lógicos** e está utilizando **{psutil.cpu_percent()}%** de sua capacidade total")
        await comando_executado(interaction, self.bot)


    # Comando de SYNC
    @group.command(name='sync', description='Sincroniza os comandos da aplicação.')
    @permissao_usar_cmd()
    async def sync(self, interaction: discord.Interaction):
        await interaction.response.send_message('Sincronizando aplicação com o Discord...')
        await self.bot.tree.sync()
        await interaction.channel.send('Aplicação sincronizada com o Discord.')
        await comando_executado(interaction, self.bot)


    # Comando de SHARD
    @group.command(name='shard', description='Mostra informações sobre os shards.')
    @permissao_usar_cmd()
    async def shard(self, interaction: discord.Interaction):
        if interaction.guild is not None:
            mensagem = f"A aplicação possui **{self.bot.shard_count} shards.** \nShard atual: **{interaction.guild.shard_id}** \nPing médio: **{round(self.bot.latency * 1000)}ms**```autohotkey"
            for shard in self.bot.latencies:
                mensagem += f"\nShard {shard[0]}: {round(shard[1] * 1000)}ms"
            mensagem += "```"
            await interaction.response.send_message(mensagem)
        else:
            mensagem = f"A aplicação possui **{self.bot.shard_count} shards.** \nShard atual: **0** \nPing médio: **{round(self.bot.latency * 1000)}ms**```autohotkey"
            for shard in self.bot.latencies:
                mensagem += f"\nShard {shard[0]}: {round(shard[1] * 1000)}ms"
            mensagem = mensagem + "```"
            await interaction.response.send_message(f"{mensagem}")
        await comando_executado(interaction, self.bot)


    # Comando de UPTIME
    @group.command(name='uptime', description='Mostra o tempo de atividade da aplicação.')
    @permissao_usar_cmd()
    async def uptime(self, interaction: discord.Interaction):
        time_now = datetime.datetime.now().timestamp()
        uptime = time_now - self.bot.time_start
        await interaction.response.send_message(f"A aplicação está online há **{int(uptime / 3600)}h {int(uptime / 60) % 60}m {int(uptime % 60)}s**")
        await comando_executado(interaction, self.bot)


    # Comando de STATUS
    @group.command(name='status', description='Mostra o status da aplicação.')
    @permissao_usar_cmd()
    async def status(self, interaction: discord.Interaction):
        config = configparser.ConfigParser()
        config.read('config.conf')
        cor_embed = int(config['CORES']['DEFAULT'])
        embed = discord.Embed(title="Status da aplicação", color=cor_embed)
        embed.set_thumbnail(url=self.bot.user.avatar)
        embed.description = f"\
        \n**Nome:** {self.bot.user.name}\
        \n**ID:** {self.bot.user.id}\
        \n**Ping:** {round(self.bot.latency * 1000)}ms \
        \n**RAM:** {psutil.virtual_memory().used / 1024 / 1024:.0f}/{psutil.virtual_memory().total / 1024 / 1024:.0f}MB ({psutil.virtual_memory().percent}%) \
        \n**CPU:** {psutil.cpu_count()} núcleos lógicos e {psutil.cpu_percent()}% de sua capacidade total \
        \n**Shards:** {self.bot.shard_count} shards \
        \n**Uptime:** {int((datetime.datetime.now().timestamp() - self.bot.time_start) / 3600)}h {int((datetime.datetime.now().timestamp() - self.bot.time_start) / 60) % 60}m {int((datetime.datetime.now().timestamp() - self.bot.time_start) % 60)}s"
        embed.set_footer(text=f"{str(self.bot.status).title()}")
        await interaction.response.send_message(embed=embed)
        await comando_executado(interaction, self.bot)


    # Comando de LOGS
    @group.command(name='logs', description='Exibe as últimas logs da aplicação.')
    @permissao_usar_cmd()
    async def logs(self, interaction: discord.Interaction):
        # Exibir ultimos 10 logs do arquivo UTF-8
        with open('logs.log', 'r', encoding='utf-8') as f:
            logs = f.read().splitlines()
            logs = logs[-20:]
            logs = '\n'.join(logs)
        await interaction.response.send_message(f"```autohotkey\n{logs}```", ephemeral=True)
        await comando_executado(interaction, self.bot)


    # Erro do comando PING
    @ping.error
    async def ping_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message("Você não tem permissão para executar esse comando.", ephemeral=True)
        else:
            await interaction.response.send_message("Ocorreu um erro ao executar o comando.", ephemeral=True)
            logging.error(f'{error}')
        await comando_executado(interaction, self.bot)


    # Erro do comando RAM
    @ram.error
    async def ram_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message("Você não tem permissão para executar esse comando.", ephemeral=True)
        else:
            await interaction.response.send_message("Ocorreu um erro ao executar o comando.", ephemeral=True)
            logging.error(f'{error}')
        await comando_executado(interaction, self.bot)


    # Erro do comando CPU
    @cpu.error
    async def cpu_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message("Você não tem permissão para executar esse comando.", ephemeral=True)
        else:
            await interaction.response.send_message("Ocorreu um erro ao executar o comando.", ephemeral=True)
            logging.error(f'{error}')
        await comando_executado(interaction, self.bot)


    # Erro do comando SYNC
    @sync.error
    async def sync_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message("Você não tem permissão para executar esse comando.", ephemeral=True)
        else:
            await interaction.response.send_message("Ocorreu um erro ao executar o comando.", ephemeral=True)
            logging.error(f'{error}')
        await comando_executado(interaction, self.bot)


    # Erro do comando SHARD
    @shard.error
    async def shard_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message("Você não tem permissão para executar esse comando.", ephemeral=True)
        else:
            await interaction.response.send_message("Ocorreu um erro ao executar o comando.", ephemeral=True)
            logging.error(f'{error}')
        await comando_executado(interaction, self.bot)


    # Erro do comando UPTIME
    @uptime.error
    async def uptime_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message("Você não tem permissão para executar esse comando.", ephemeral=True)
        else:
            await interaction.response.send_message("Ocorreu um erro ao executar o comando.", ephemeral=True)
            logging.error(f'{error}')
        await comando_executado(interaction, self.bot)


    # Erro do comando STATUS
    @status.error
    async def status_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message("Você não tem permissão para executar esse comando.", ephemeral=True)
        else:
            await interaction.response.send_message("Ocorreu um erro ao executar o comando.", ephemeral=True)
            logging.error(f'{error}')
        await comando_executado(interaction, self.bot)

    
    # Erro do comando LOGS
    @logs.error
    async def logs_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message("Você não tem permissão para executar esse comando.", ephemeral=True)
        else:
            await interaction.response.send_message("Ocorreu um erro ao executar o comando.", ephemeral=True)
            logging.error(f'{error}')
        await comando_executado(interaction, self.bot)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(DevCommands(bot))