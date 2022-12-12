import discord
from discord import app_commands
from discord.ext import commands
from src.others.comando_executado import comando_executado
import logging

class Limpar(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Carregado: {__name__}')


    @app_commands.command(name='limpar', description='Limpar mensagens do canal.')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.bot_has_permissions(manage_messages=True)
    async def limpar(self, interaction: discord.Interaction, quantidade: int, canal: discord.TextChannel = None, usuário: discord.User = None):
        await interaction.response.defer(ephemeral=True)
        if quantidade > 100:
            await interaction.followup.send("Você não pode limpar mais de 100 mensagens de uma vez.", ephemeral=True)
        elif quantidade <= 1:
            await interaction.followup.send("Você precisa limpar pelo menos 2 mensagens.", ephemeral=True)
        else:
            if canal is None:
                if usuário is None:
                    await interaction.channel.purge(limit=quantidade, bulk=True, reason=f'Solicitado por {interaction.user.name}#{interaction.user.discriminator}')
                    await interaction.followup.send(f"Limpei **{quantidade}** mensagens neste canal.", ephemeral=True)
                else:
                    def check(m):
                        return m.author == usuário
                    await interaction.channel.purge(limit=quantidade, check=check, bulk=True, reason=f"Solicitado por {interaction.user.name}#{interaction.user.discriminator}")
                    await interaction.followup.send(f"Limpei **{quantidade}** mensagens do usuário **{usuário.display_name}** neste canal.", ephemeral=True)
            else:
                if usuário is None:
                    await canal.purge(limit=quantidade, bulk=True, reason=f"Solicitado por {interaction.user.name}#{interaction.user.discriminator}")
                    await interaction.followup.send(f"Limpei **{quantidade}** mensagens do canal **{canal.mention}**.", ephemeral=True)
                else:
                    def check(m):
                        return m.author == usuário
                    await canal.purge(limit=quantidade, check=check, bulk=True, reason=f"Solicitado por {interaction.user.name}#{interaction.user.discriminator}")
                    await interaction.followup.send(f"Limpei **{quantidade}** mensagens do usuário **{usuário.display_name}** no canal **{canal.mention}**.", ephemeral=True)
        await comando_executado(interaction, self.bot)


    @limpar.error
    async def limpar_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.followup.send("Você não tem permissão para executar esse comando.", ephemeral=True)
        elif isinstance(error, app_commands.BotMissingPermissions):
            await interaction.followup.send("O bot não tem permissão para executar esse comando, verifique se ele tem a permissão de gerenciar mensagens.", ephemeral=True)
        else:
            await interaction.followup.send("Ocorreu um erro ao executar o comando.", ephemeral=True)
            logging.error(f'{error}')
        await comando_executado(interaction, self.bot)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Limpar(bot))