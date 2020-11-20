import json

from cogs.filloas import Filloas
from cogs.admin_tools import *
from cogs.events import Events
from cogs.voice import Voice

import discord

#Cargar el token del archivo json
with open("token.json") as file:
    data = json.load(file)
token = data['token']

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

bot.run(token)