from discord.ext import commands
from src.database.firebase import FirebaseDB


class Sync(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[INFO] Carregado: {__name__}')


    @commands.command(name='sync', description='Sincroniza os comandos da aplicação.')
    @commands.is_owner()
    async def sync(self, ctx: commands.Context):
        await FirebaseDB.contador_comandos(self.bot.database)
        await ctx.send('Sincronizando aplicação com o Discord...')
        await ctx.bot.tree.sync()
        await ctx.send('Aplicação sincronizada com o Discord.')


    @sync.error
    async def sync_error(self, ctx: commands.Context, error):
        await FirebaseDB.contador_comandos(self.bot.database)
        if isinstance(error, commands.NotOwner):
            await ctx.send('Você não tem permissão para executar esse comando.')
        else:
            await ctx.send('Ocorreu um erro ao executar o comando.')
            print(f'[ERRO] {error}')


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Sync(bot))