from discord.ext import commands
import configparser
import discord

class NovoServidor(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[INFO] Carregado arquivo: {__name__}')


    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        config = configparser.ConfigParser()
        config.read("config.ini")      
        cor = config.getint("CORES", "COR_PRINCIPAL")
        canal_id = config.getint("IDS", "CANAL_LOGS_NOVO_SERVIDOR")
        
        embed = discord.Embed(
            title = "A aplicação entrou em um novo servidor!",
            color = cor
        )   
        embed.add_field(name="Nome do servidor:", value=guild.name, inline=True)
        embed.add_field(name="ID do servidor:", value=guild.id, inline=True)
        embed.add_field(name="Dono do servidor:", value=guild.owner, inline=True)
        embed.add_field(name="ID do dono do servidor:", value=guild.owner.id, inline=True)
        embed.add_field(name="Membros:", value=guild.member_count, inline=True)
        embed.add_field(name="Criado em:", value=guild.created_at.strftime("%d/%m/%Y %H:%M:%S"), inline=True)

        embed.set_footer(text=f"ID do servidor: {guild.id}")

        if guild.icon == None:
            pass # Futuramente, colocar uma imagem padrão
        else:
            embed.set_thumbnail(url=guild.icon)

        print(f'[INFO] Aplicação entrou em um novo servidor: {guild.name} - {guild.id}')
        canal = self.bot.get_channel(canal_id)
        await canal.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(NovoServidor(bot))