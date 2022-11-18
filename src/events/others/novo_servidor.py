from discord.ext import commands
import dotenv
import os
import discord
from datetime import timezone

class NovoServidor(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[INFO] Carregado arquivo: {__name__}')


    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        dotenv.load_dotenv()
        cor_embed = int(os.getenv('COR_PRINCIPAL_EMBEDS'))
        canal_id = int(os.getenv('CANAL_LOGS_NOVO_SERVIDOR_ID'))
        
        embed = discord.Embed(
            title = "A aplicação entrou em um novo servidor!",
            color = cor_embed
        )   
        embed.add_field(name="Nome do servidor:", value=guild.name, inline=True)
        embed.add_field(name="ID do servidor:", value=guild.id, inline=True)
        embed.add_field(name="Dono do servidor:", value=guild.owner, inline=True)
        embed.add_field(name="ID do dono do servidor:", value=guild.owner.id, inline=True)
        embed.add_field(name="Membros:", value=guild.member_count, inline=True)
        embed.add_field(name="Criado em:", value=guild.created_at.strftime("%d/%m/%Y %H:%M:%S"), inline=True)

        bot_member = guild.get_member(self.bot.user.id)
        horario_entrada = bot_member.joined_at.replace(tzinfo=timezone.utc).astimezone(tz=None)
        embed.set_footer(text=f"Entrou em {horario_entrada.strftime('%d/%m/%Y às %H:%M:%S')}")

        if guild.icon == None:
            embed.set_thumbnail(url="https://i.imgur.com/bWJ0Z2U.png")
        else:
            embed.set_thumbnail(url=guild.icon)

        print(f'[INFO] Aplicação entrou em um novo servidor: {guild.name} - {guild.id}')
        canal = self.bot.get_channel(canal_id)
        await canal.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(NovoServidor(bot))