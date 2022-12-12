from discord.ext import commands
import discord
from firebase_admin import db
import random


class ExperienciaEvento(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.cooldown = commands.CooldownMapping.from_cooldown(3.0, 30.0, commands.BucketType.user)


    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[INFO] Carregado: {__name__}')


    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        bucket = self.cooldown.get_bucket(message)
        retry_after = bucket.update_rate_limit()

        if retry_after:
            # print(f'[DEBUG] {message.author} está em cooldown de {retry_after:.2f} segundos para ganhar experiência.')
            pass
        else:
            if message.author.bot:
                return
            
            request = db.reference('/servidores/' + str(message.guild.id) + '/usuarios/' + str(message.author.id) + '/experiencia')
            xp_gerado = random.randint(10, 50)

            if request.get() is None:
                request.set({
                    'level': 1,
                    'xp': 0,
                })
                
            try:
                xp_atual = request.get()['xp']
            except:
                xp_atual = 0

            try:
                level_atual = request.get()['level']
            except:
                level_atual = 1

            xp_atual += xp_gerado
            xp_para_proximo_level = int(5 * (level_atual ** 2) + 50 * level_atual + 100)
            
            # print(f'[DEBUG] {message.author} ganhou {xp_gerado} de XP.')
            # print(f'[DEBUG] {message.author} está no level {level_atual} com {xp_atual} de XP.')
            # print(f'[DEBUG] {message.author} precisa de {xp_para_proximo_level} de XP para subir de level.')

            if xp_atual >= xp_para_proximo_level:
                xp_atual -= xp_para_proximo_level
                level_atual += 1

            request.update({
                'xp': xp_atual,
                'level': level_atual,
            })


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ExperienciaEvento(bot))