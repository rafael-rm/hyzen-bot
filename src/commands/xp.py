import discord
from discord import app_commands
from discord.ext import commands
from src.functions.comando_executado import comando_executado
from firebase_admin import db
import logging


class Xp(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Carregado: {__name__}')


    @app_commands.command(name='xp', description='Veja seu nível e experiência.')
    @app_commands.guild_only()
    async def xp(self, interaction: discord.Interaction, membro: discord.User = None):
        if membro is None:
            user = interaction.user
        else:
            user = membro

        request = db.reference('/servidores/' + str(interaction.guild.id) + '/usuarios/' + str(user.id) + '/experiencia')
        dados = request.get()

        if dados is None:
            dados = {
                'level': 1,
                'xp': 0
            }

        try: 
            level_atual = dados['level']
        except:
            level_atual = 1
        try:
            xp_atual = dados['xp']
        except:
            xp_atual = 0

        xp_para_proximo_level = int(5 * (level_atual ** 2) + 50 * level_atual + 100) - xp_atual

        if xp_para_proximo_level < 0:
            xp_para_proximo_level = 0

        if user.id == interaction.user.id:
            await interaction.response.send_message(f'Você está no nível **{level_atual}** com **{xp_atual}** de experiência. \nVocê precisa de **{xp_para_proximo_level}** de experiência para subir de nível.')
        else:
            await interaction.response.send_message(f'{user.display_name} está no nível **{level_atual}** com **{xp_atual}** de experiência. \nEle precisa de **{xp_para_proximo_level}** de experiência para subir de nível.')

        await comando_executado(interaction, self.bot)

    
    @xp.error
    async def xp_error(self, interaction: discord.Interaction, error):
        await comando_executado(interaction, self.bot)
        await interaction.response.send_message('Ocorreu um erro ao executar este comando.')
        logging.error(f'Erro ao executar comando: {error}')


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Xp(bot))