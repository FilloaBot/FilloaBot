import json
import logging
import sys

import discord
from discord.ext import commands

#Cargar el token del archivo json
with open("token.json") as file:
    data = json.load(file)
token = data['bot_token']

#Activar el logging
logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename = "discord.log", encoding = "UTF-8", mode = 'w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.members = True
intents.reactions = True
intents.messages = True
intents.emojis = True
bot = commands.Bot(command_prefix = '?', description = "Bot para diversos propositos")

bot.cogs_list = [
    "cogs.filloas",
    "cogs.jokes",
    "cogs.admin_tools",
    "cogs.events",
    "cogs.voice",
    "cogs.economy"
]

for cog in bot.cogs_list:
    bot.load_extension(cog)

bot.run(token)