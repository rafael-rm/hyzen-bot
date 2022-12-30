from discord.ext import commands
from src.functions.comando_executado import comando_executado
from src.functions.comando_executado import tentativa_comando_critico
import logging
import configparser


class Sync(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Carregado: {__name__}')


    def permissao_usar_cmd():
        def verificar_desenvolvedores(ctx: commands.Context) -> bool:
            config = configparser.ConfigParser()
            config.read('config.conf')
            desenvolvedores_ids = [e.strip() for e in config.get('IDS', 'DESENVOLVEDORES_IDS').split(',')]
            for desenvolvedor_id in desenvolvedores_ids:
                desenvolvedor_id = int(desenvolvedor_id)
                if ctx.author.id == desenvolvedor_id:
                    return True
        return commands.check(verificar_desenvolvedores)


    @commands.command(name='sync', description='Sincroniza os comandos da aplicação.')
    @permissao_usar_cmd()
    async def sync(self, ctx: commands.Context):
        await comando_executado(ctx, self.bot)
        await ctx.send('Sincronizando aplicação com o Discord...')
        logging.info('Sincronizando aplicação com o Discord...')
        await ctx.bot.tree.sync()
        await ctx.send('Aplicação sincronizada com o Discord.')
        logging.info('Aplicação sincronizada com o Discord.')


    @sync.error
    async def sync_error(self, ctx: commands.Context, error):
        await comando_executado(ctx, self.bot)
        if isinstance(error, commands.CheckFailure):
            await tentativa_comando_critico(ctx, self.bot)
            await ctx.send('Você não tem permissão para executar este comando.')
        else:
            await ctx.send('Ocorreu um erro ao executar este comando.')
            logging.error(f'Erro ao executar comando: {error}')


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Sync(bot))