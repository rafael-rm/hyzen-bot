from discord.ext import commands


class Sync(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[INFO] Carregado arquivo: {__name__}')


    @commands.command(name='sync', description='Sincroniza os comandos da aplicação.')
    @commands.is_owner()
    async def sync(self, ctx: commands.Context):
        await ctx.send('Sincronizando aplicação com o Discord...')

        sync_msg = await ctx.bot.tree.sync()
        await ctx.send(f'```{sync_msg}```')


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Sync(bot))
