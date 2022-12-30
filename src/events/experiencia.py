from discord.ext import commands
import discord
from firebase_admin import db
import random
import logging


class ExperienciaEvento(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.cooldown = commands.CooldownMapping.from_cooldown(3.0, 30.0, commands.BucketType.user)


    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Carregado: {__name__}')


    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):

        if message.guild is None:
            return

        bucket = self.cooldown.get_bucket(message)
        retry_after = bucket.update_rate_limit()

        if retry_after: # Se o usuário estiver no cooldown, o bot não irá executar o código abaixo.
            pass
        else:
            if message.author.bot:
                return
            
            request = db.reference('/servidores/' + str(message.guild.id) + '/usuarios/' + str(message.author.id) + '/experiencia')
            dados = request.get()

            xp_gerado = random.randint(10, 50)

            if dados is None:
                dados = {
                    'level': 1,
                    'xp': 0
                }
                
            try: 
                level_atual = dados['level']
            except:
                level_atual = 1
            try:
                xp_atual = dados['xp']
            except:
                xp_atual = 0

            xp_atual += xp_gerado
            xp_para_proximo_level = int(5 * (level_atual ** 2) + 50 * level_atual + 100)

            if xp_atual >= xp_para_proximo_level:
                xp_atual -= xp_para_proximo_level
                level_atual += 1
                logging.info(f'{message.author.id} subiu para o level {level_atual} no servidor {message.guild.id}.')
                request.update({
                    'xp': xp_atual,
                    'level': level_atual,
                })
            else:
                request.update({
                    'xp': xp_atual,
                })


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ExperienciaEvento(bot))