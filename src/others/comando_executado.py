from src.database.firebase import FirebaseDB
import logging


async def comando_executado(cmd, bot):
    await FirebaseDB.contador_comandos(bot.database)
    logging.info(f'Comando \'{cmd.command.name}\' executado por {cmd.user.id} no servidor {cmd.guild.id}')