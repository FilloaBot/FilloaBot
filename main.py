#!/usr/bin/python3
#-*- encoding: UTF-8 -*-

import json
import logging
import sys

import discord
from discord.ext import commands

#Set up the token
with open("token.json") as file:
    data = json.load(file)
token = data['bot_token']

#Setting up the loggin
logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename = "discord.log", encoding = "UTF-8", mode = 'w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

#Activating some stuff
intents = discord.Intents.default()
intents.members = True
intents.reactions = True
intents.messages = True
intents.emojis = True

bot = commands.Bot(command_prefix = '?', description = "El mejor bot del mundo manines")
bot.remove_command("help") #Remove the default help command

#Loading cogs
bot.cogs_list = [
    "cogs.filloas",
    "cogs.ubports",
    "cogs.jokes",
    "cogs.admin_tools",
    "cogs.events",
    "cogs.voice",
    "cogs.economy"
]

for cog in bot.cogs_list:
    bot.load_extension(cog)

bot.run(token)