import discord
from discord import app_commands
from discord.ext import commands
from src.database.firebase import FirebaseDB


class Clear(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[INFO] Carregado arquivo: {__name__}')


    @app_commands.command(name='clear', description='Limpar mensagens do canal.')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.bot_has_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, quantidade: int, canal: discord.TextChannel = None):
        await FirebaseDB.contador_comandos(self.bot.database)
        if quantidade > 100:
            await interaction.response.send_message('Você não pode apagar mais de 100 mensagens por vez.', ephemeral=True)
        elif quantidade < 1:
            await interaction.response.send_message('Você não pode apagar menos de 1 mensagem.', ephemeral=True)
        else:
            if canal is None:
                await interaction.response.send_message(f'Um total de **{quantidade}** mensagens foram apagadas.', ephemeral=True, delete_after=5)
                await interaction.channel.purge(limit=quantidade)
            else:
                await interaction.response.send_message(f'Um total de **{quantidade}** mensagens foram apagadas do canal {canal.mention}.', ephemeral=True, delete_after=5)
                await canal.purge(limit=quantidade)


    @clear.error
    async def clear_error(self, interaction: discord.Interaction, error):
        await FirebaseDB.contador_comandos(self.bot.database)
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message("Você não tem permissão para executar esse comando.", ephemeral=True)
        elif isinstance(error, app_commands.BotMissingPermissions):
            await interaction.response.send_message("O bot não tem permissão para executar esse comando, verifique se ele tem a permissão de gerenciar mensagens.", ephemeral=True)
        else:
            await interaction.response.send_message("Ocorreu um erro ao executar o comando.", ephemeral=True)
            print(error)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Clear(bot))