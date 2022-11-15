from discord.ext import commands


class NovoServidor(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[INFO] Carregado arquivo: {__name__}')


    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        print(f'[INFO] Aplicação entrou em um novo servidor: {guild.name} - {guild.id}')


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(NovoServidor(bot))