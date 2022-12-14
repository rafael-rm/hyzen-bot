from discord.ext import commands
import logging

class StartLog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Carregado: {__name__}')


    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Aplicação iniciada com sucesso em {self.bot.user.name}#{self.bot.user.discriminator} ({self.bot.user.id})')
        logging.info(f'Total de servidores: {len(self.bot.guilds)}')


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(StartLog(bot))