from discord.ext import commands
import discord
from firebase_admin import db
import random


class ExperienceEvent(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.cooldown = commands.CooldownMapping.from_cooldown(5.0, 60.0, commands.BucketType.user)


    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[INFO] Carregado arquivo: {__name__}')


    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        bucket = self.cooldown.get_bucket(message)
        retry_after = bucket.update_rate_limit()

        if retry_after:
            # print(f'[INFO] {message.author} está em cooldown de {retry_after:.2f} segundos.')
            pass
        else:
            if message.author.bot:
                return
            
            request = db.reference('/users/' + str(message.author.id) + '/experience')
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

            xp_atual += xp_gerado

            request.update({
                'xp': xp_atual,
            })


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ExperienceEvent(bot))