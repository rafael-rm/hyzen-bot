import logging
from firebase_admin import db
import discord


async def comando_executado(comando, bot):
    if type(comando) is discord.Interaction: # Verifica se o comando foi executado por uma interação.
        autor = comando.user
    else:
        autor = comando.author

    if comando.guild is None: # Verifica se o comando foi executado em um servidor.
        local = 'via DM'
    else:
        local = f'no servidor {comando.guild.id}' 

    logging.info(f'Comando \'{comando.command.name}\' executado por {autor.id} {local}.')
    await contador_comandos(bot)


async def tentativa_comando_critico(comando, bot):
        if type(comando) is discord.Interaction: # Verifica se o comando foi executado por uma interação.
            autor = comando.user
        else:
            autor = comando.author
    
        if comando.guild is None: # Verifica se o comando foi executado em um servidor.
            local = 'via DM'
        else:
            local = f'no servidor {comando.guild.id}' 

        logging.warn(f'Tentativa de execução de comando crítico ({comando.command.name}) por {autor.id} {local}.')


async def contador_comandos(bot):  
    bot.cache_comandos_executados += 1 
    if bot.cache_comandos_executados >= 5:
        request = db.reference('/global/comandos-executados')
        if request.get() is None:
            request.set(bot.cache_comandos_executados)
        else:
            request.set(request.get() + bot.cache_comandos_executados)
        bot.cache_comandos_executados = 0