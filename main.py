import json
import logging

from cogs.filloas import Filloas
from cogs.admin_tools import Admin_tools
from cogs.events import Events
from cogs.voice import Voice
from cogs.economy import Economy

import discord
from discord.ext import commands

#Cargar el token del archivo json
with open("token.json") as file:
    data = json.load(file)
token = data['token']

#Activar el logging
logger = logging.getLogger("discord")
logger.setlevel(logging.DEBUG)
handler = logging.FileHandler(filename = "discord.log", encoding = "UTF-8", mode = 'w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logging.addHandler(handler)

intents = discord.Intents.default()
intents.members = True
intents.reactions = True
intents.messages = True
intents.emojis = True
bot = commands.Bot(command_prefix = '?', description = "Bot para diversos propositos")

bot.add_cog(Filloas(bot))
bot.add_cog(Admin_tools(bot))
bot.add_cog(Events(bot))
bot.add_cog(Voice(bot))
bot.add_cog(Economy(bot))

bot.run(token)