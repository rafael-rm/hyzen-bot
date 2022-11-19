import discord
from discord import app_commands
from discord.ext import commands
from src.database.firebase import FirebaseDB
import dotenv
import os


class Say(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[INFO] Carregado arquivo: {__name__}')


    @app_commands.command(name='say', description='Enviar embed com uma mensagem através do bot.')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.bot_has_permissions(embed_links=True)
    async def say(self, interaction: discord.Interaction, *, mensagem: str):
        dotenv.load_dotenv()
        cor_embed = int(os.getenv('COR_PRINCIPAL_EMBEDS'))
        embed = discord.Embed(
            title = '',
            description = mensagem,
            color = cor_embed,
            timestamp = interaction.created_at,
        )

        if interaction.user.avatar:
            embed.set_footer(text=f'Enviar por {interaction.user.name}#{interaction.user.discriminator}', icon_url=interaction.user.avatar)
        else:
            embed.set_footer(text=f'Enviado por {interaction.user.name}#{interaction.user.discriminator}', icon_url=interaction.user.default_avatar)

        await interaction.channel.send(embed=embed)
        await interaction.response.send_message("Comando executado com sucesso!", ephemeral=True, delete_after=3)
        await FirebaseDB.contador_comandos(self.bot.database)


    @say.error
    async def say_error(self, interaction: discord.Interaction, error):
        await FirebaseDB.contador_comandos(self.bot.database)
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message("Você não tem permissão para executar esse comando.", ephemeral=True)
        elif isinstance(error, app_commands.BotMissingPermissions):
            await interaction.response.send_message("O bot não tem permissão para executar esse comando, verifique se ele tem a permissão de enviar embeds.", ephemeral=True)
        else:
            await interaction.response.send_message("Ocorreu um erro ao executar o comando.", ephemeral=True)
            print(error)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Say(bot))