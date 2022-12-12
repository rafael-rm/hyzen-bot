import discord
from discord import app_commands
from discord.ext import commands
from src.database.firebase import FirebaseDB
from firebase_admin import db
import configparser


class AutoRoleCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    group = app_commands.Group(name="autorole", description="Comandos do cargo automático")


    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[INFO] Carregado: {__name__}')


    # Comando de ADICIONAR
    @group.command(name='adicionar', description='Adiciona um cargo ao autorole.')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.checks.bot_has_permissions(manage_roles=True)
    async def adicionar(self, interaction: discord.Interaction, cargo: discord.Role):
        # Verificar se o cargo é menor que o cargo do bot
        if cargo.position > interaction.guild.me.top_role.position:
            await interaction.response.send_message('O cargo é maior que o meu cargo. Não posso adicionar.')
            await FirebaseDB.contador_comandos(self.bot.database)
            return

        # Verificar se o cargo é menor que o cargo do usuário
        if cargo.position > interaction.user.top_role.position:
            await interaction.response.send_message('O cargo é maior que o seu cargo. Não posso adicionar.')
            await FirebaseDB.contador_comandos(self.bot.database)
            return

        # Verificar se o cargo já no banco de dados
        request = db.reference('/servidores/' + str(interaction.guild.id) + '/autorole').get()
        if request is not None:
            for i in range(0, len(request)):
                if request[i] == str(cargo.id):
                    await interaction.response.send_message('O cargo já está na lista de autorole.')
                    await FirebaseDB.contador_comandos(self.bot.database)
                    return
        if request is None:
            request = []
        request.append(str(cargo.id))
        db.reference('/servidores/' + str(interaction.guild.id) + '/autorole').set(request)
        await interaction.response.send_message('Cargo adicionado com sucesso.')
        await FirebaseDB.contador_comandos(self.bot.database)


    # Comando de REMOVER
    @group.command(name='remover', description='Remove um cargo ao autorole.')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(manage_roles=True)
    async def remover(self, interaction: discord.Interaction, cargo: discord.Role):
        request = db.reference('/servidores/' + str(interaction.guild.id) + '/autorole').get()
        if request is not None:
            for i in range(0, len(request)):
                if request[i] == str(cargo.id):
                    request.pop(i)
                    db.reference('/servidores/' + str(interaction.guild.id) + '/autorole').set(request)
                    await interaction.response.send_message('Cargo removido com sucesso.')
                    await FirebaseDB.contador_comandos(self.bot.database)
                    return
        await interaction.response.send_message('O cargo não está na lista de autorole.')
        await FirebaseDB.contador_comandos(self.bot.database)


    # Comando de LISTAR
    @group.command(name='listar', description='Lista os cargos do autorole.')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(manage_roles=True)
    async def listar(self, interaction: discord.Interaction):
        request = db.reference('/servidores/' + str(interaction.guild.id) + '/autorole').get()
        if request is not None:
            cargos = ''
            for i in range(0, len(request)):
                cargos += f'<@&{request[i]}>\n'
            config = configparser.ConfigParser()
            config.read('config.conf')
            cor_embed = int(config['CORES']['DEFAULT'])
            embed = discord.Embed(title='', description=cargos, color=cor_embed)
            embed.set_author(name='Cargos configurados para serem adicionados quando um novo usuário entrar no servidor.')
            await interaction.response.send_message(embed=embed)
            await FirebaseDB.contador_comandos(self.bot.database)
            return
        await interaction.response.send_message('Não há cargos no autorole.')
        await FirebaseDB.contador_comandos(self.bot.database)
        

    # Erro do comando de ADICIONAR
    @adicionar.error
    async def adicionar_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message('Você não tem permissão para executar este comando.')
        elif isinstance(error, app_commands.BotMissingPermissions):
            await interaction.response.send_message('Eu não tenho permissão para gerenciar cargos neste servidor.')
        elif isinstance(error, app_commands.RoleNotFound):
            await interaction.response.send_message('Cargo não encontrado.')
        else:
            await interaction.response.send_message('Ocorreu um erro ao executar este comando.')
            print(f'[ERRO] {error}')
        await FirebaseDB.contador_comandos(self.bot.database)


    # Erro do comando de REMOVER
    @remover.error
    async def remover_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message('Você não tem permissão para executar este comando.')
        else:
            await interaction.response.send_message('Ocorreu um erro ao executar este comando.')
            print(f'[ERRO] {error}')
        await FirebaseDB.contador_comandos(self.bot.database)


    # Erro do comando de LISTAR
    @listar.error
    async def listar_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message('Você não tem permissão para executar este comando.')
        else:
            await interaction.response.send_message('Ocorreu um erro ao executar este comando.')
            print(f'[ERRO] {error}')
        await FirebaseDB.contador_comandos(self.bot.database)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AutoRoleCommands(bot))