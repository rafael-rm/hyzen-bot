import discord
from discord import app_commands
from discord.ext import commands


class Clear(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[INFO] Carregado arquivo: {__name__}')


    @app_commands.command(name='limpar', description='Limpar mensagens do canal.')
    @commands.has_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, quantidade: int, canal: discord.TextChannel = None):
        if quantidade > 100:
            await interaction.response.send_message('Você não pode apagar mais de 100 mensagens por vez.', ephemeral=True)
        elif quantidade < 1:
            await interaction.response.send_message('Você não pode apagar menos de 1 mensagem.', ephemeral=True)
        else:
            if canal is None:
                await interaction.response.send_message(f'Um total de **{quantidade}** mensagens foram apagadas.', ephemeral=True)
                await interaction.channel.purge(limit=quantidade)
            else:
                await interaction.response.send_message(f'Um total de **{quantidade}** mensagens foram apagadas do canal {canal.mention}.', ephemeral=True)
                await canal.purge(limit=quantidade)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Clear(bot))
