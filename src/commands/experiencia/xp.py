import discord
from discord import app_commands
from discord.ext import commands
from src.database.firebase import FirebaseDB
from firebase_admin import db


class Xp(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[INFO] Carregado: {__name__}')


    @app_commands.command(name='xp', description='Veja seu nível e experiência.')
    async def xp(self, interaction: discord.Interaction, membro: discord.User = None):
        if membro is None:
            user = interaction.user
        else:
            user = membro

        request = db.reference('/servidores/' + str(interaction.guild.id) + '/usuarios/' + str(user.id) + '/experiencia')
        if request.get() is None:
            request.set({
                'xp': 0,
                'level': 1,
            })

        try:
            request.get()['xp']
        except:
            request.update({
                'xp': 0
            })

        try:
            request.get()['level']
        except:
            request.update({
                'level': 1
            })

        level_atual = request.get()['level']
        xp_atual = request.get()['xp']
        xp_para_proximo_level = int(5 * (level_atual ** 2) + 50 * level_atual + 100) - xp_atual

        if user.id == interaction.user.id:
            await interaction.response.send_message(f'Você está no nível **{level_atual}** com **{xp_atual}** de experiência. \nVocê precisa de **{xp_para_proximo_level}** de experiência para subir de nível.')
        else:
            await interaction.response.send_message(f'{user.display_name} está no nível **{level_atual}** com **{xp_atual}** de experiência. \nEle precisa de **{xp_para_proximo_level}** de experiência para subir de nível.')

        await FirebaseDB.contador_comandos(self.bot.database)

    
    @xp.error
    async def xp_error(self, interaction: discord.Interaction, error):
        await FirebaseDB.contador_comandos(self.bot.database)
        await interaction.response.send_message("Ocorreu um erro ao executar o comando.", ephemeral=True)
        print(f'[ERRO] {error}')


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Xp(bot))