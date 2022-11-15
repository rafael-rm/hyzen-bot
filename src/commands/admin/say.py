import discord
from discord import app_commands
from discord.ext import commands


COLOR = "2f3136"


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
        embed = discord.Embed(
            title = '',
            description = mensagem,
            color = int(COLOR, 16),
            timestamp = interaction.created_at,
        )
        embed.set_footer(text=f'Enviado por {interaction.user.name}', icon_url=interaction.user.avatar)
        await interaction.channel.send(embed=embed)
        await interaction.response.send_message("Comando executado com sucesso!", ephemeral=True, delete_after=3)

    
    @say.error
    async def say_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message("Você não tem permissão para executar esse comando.", ephemeral=True)
        elif isinstance(error, app_commands.BotMissingPermissions):
            await interaction.response.send_message("O bot não tem permissão para executar esse comando, verifique se ele tem a permissão de enviar embeds.", ephemeral=True)
        else:
            await interaction.response.send_message("Ocorreu um erro ao executar o comando.", ephemeral=True)



async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Say(bot))
