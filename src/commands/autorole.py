import discord
from discord import app_commands
from discord.ext import commands
from src.functions.comando_executado import comando_executado
from firebase_admin import db
import configparser
import logging


class AutoRoleCommands(commands.GroupCog, name="autorole", description="Comandos do cargo automático"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f'Carregado: {__name__}')


    # Comando de ADICIONAR
    @app_commands.command(name='adicionar', description='Adiciona um cargo ao autorole.')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.checks.bot_has_permissions(manage_roles=True)
    async def adicionar(self, interaction: discord.Interaction, cargo: discord.Role):

        # Verificar se o cargo mencionado foi o @everyone ou @here
        if cargo.id == interaction.guild.id:
            await interaction.response.send_message('Não posso adicionar o cargo **everyone** no autorole.')
            await comando_executado(interaction, self.bot)
            return

        # Verificar se o cargo nao é um cargo de bot
        if cargo.managed or cargo.is_bot_managed():
            await interaction.response.send_message('Não posso adicionar um cargo de bot no autorole.')
            await comando_executado(interaction, self.bot)
            return

        # Verificar se o cargo a ser adicionado não é maior que o cargo do bot
        if cargo.position >= interaction.guild.me.top_role.position:
            await interaction.response.send_message('O cargo que deseja adicionar no autorole é maior ou igual ao meu cargo. Não posso adicionar.')
            await comando_executado(interaction, self.bot)
            return

        # Verificar se o cargo é menor que o cargo do usuário ou ele possui permissão de administrador
        if cargo.position > interaction.user.top_role.position and not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message('O cargo que deseja adicionar no autorole é maior que o seu cargo. Não posso adicionar.')
            await comando_executado(interaction, self.bot)
            return

        request = db.reference('/servidores/' + str(interaction.guild.id) + '/autorole').get()
    
        # Verificar se o cargo já no banco de dados
        if request is not None:
            for i in range(0, len(request)):
                if request[i] == str(cargo.id):
                    await interaction.response.send_message('O cargo já foi adicionado ao autorole.')
                    await comando_executado(interaction, self.bot)
                    return

        if request is None:
            request = []

        request.append(str(cargo.id))
        db.reference('/servidores/' + str(interaction.guild.id) + '/autorole').set(request)
        await interaction.response.send_message('Cargo adicionado com sucesso.')
        await comando_executado(interaction, self.bot)


    # Comando de REMOVER
    @app_commands.command(name='remover', description='Remove um cargo ao autorole.')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(manage_roles=True)
    async def remover(self, interaction: discord.Interaction, cargo: discord.Role):
        request = db.reference('/servidores/' + str(interaction.guild.id) + '/autorole').get()
        if request is not None:
            for i in range(0, len(request)):
                if request[i] == str(cargo.id):
                    request.pop(i)
                    db.reference('/servidores/' + str(interaction.guild.id) + '/autorole').set(request)
                    await interaction.response.send_message('Cargo removido do autorole com sucesso.')
        else:
            await interaction.response.send_message('O cargo não está no autorole.')
        await comando_executado(interaction, self.bot)


    # Comando de LISTAR
    @app_commands.command(name='listar', description='Lista os cargos do autorole.')
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
        else: 
            await interaction.response.send_message('Não há cargos no autorole.')
        await comando_executado(interaction, self.bot)
        

    # Erro do comando de ADICIONAR
    @adicionar.error
    async def adicionar_error(self, interaction: discord.Interaction, error):
        await comando_executado(interaction, self.bot)
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message('Você não tem permissão para executar este comando.')
        elif isinstance(error, app_commands.BotMissingPermissions):
            await interaction.response.send_message('Eu não tenho permissão para gerenciar cargos neste servidor.')
        else:
            await interaction.response.send_message('Ocorreu um erro ao executar este comando.')
            logging.error(f'{error}')


    # Erro do comando de REMOVER
    @remover.error
    async def remover_error(self, interaction: discord.Interaction, error):
        await comando_executado(interaction, self.bot)
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message('Você não tem permissão para executar este comando.')
        else:
            await interaction.response.send_message('Ocorreu um erro ao executar este comando.')
            logging.error(f'{error}')


    # Erro do comando de LISTAR
    @listar.error
    async def listar_error(self, interaction: discord.Interaction, error):
        await comando_executado(interaction, self.bot)
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message('Você não tem permissão para executar este comando.')
        else:
            await interaction.response.send_message('Ocorreu um erro ao executar este comando.')
            logging.error(f'{error}')


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AutoRoleCommands(bot))