import discord
from discord import app_commands
from discord.ext import commands
from src.others.comando_executado import comando_executado
from firebase_admin import db
import datetime
import random
import logging


class Daily(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Carregado: {__name__}')


    @app_commands.command(name='daily', description='Receba recompensas diariamente.')
    async def daily(self, interaction: discord.Interaction):
        request = db.reference('/usuarios/' + str(interaction.user.id) + '/economia')
        timestamp_atual = datetime.datetime.now().timestamp()
        hyzen_coin = random.randint(500, 2000)

        if request.get() is None:
            request.set({
                'hyzen-coin': 0,
                'timestamp-ultimo-daily': 0
            })
            
        try:
            request.get()['hyzen-coin']
        except:
            request.update({
                'hyzen-coin': 0
            })

        try:
            timestamp_ultimo_daily = request.get()['timestamp-ultimo-daily']
        except:
            timestamp_ultimo_daily = 0

        if timestamp_atual - timestamp_ultimo_daily >= 86400:
            request.update({
                'hyzen-coin': request.get()['hyzen-coin'] + hyzen_coin,
                'timestamp-ultimo-daily': timestamp_atual
            })
            await interaction.response.send_message(f'Você recebeu **{hyzen_coin} HC**! Você pode receber novamente em **24 horas** \nUsuários **VIPs** recebem até 2.5x mais recompensas.')
        else:
            horas_restantes = int((86400 - (timestamp_atual - timestamp_ultimo_daily)) / 3600)
            minutos_restantes = int(((86400 - (timestamp_atual - timestamp_ultimo_daily)) % 3600) / 60)
            segundos_restantes = int(((86400 - (timestamp_atual - timestamp_ultimo_daily)) % 3600) % 60)
            await interaction.response.send_message(f"Você já recebeu seu daily hoje, volte em {horas_restantes} horas, {minutos_restantes} minutos e {segundos_restantes} segundos.")
        
        await comando_executado(interaction, self.bot)


    @daily.error
    async def daily_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message("Ocorreu um erro ao executar o comando.", ephemeral=True)
        logging.error(f'{error}')
        await comando_executado(interaction, self.bot)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Daily(bot))