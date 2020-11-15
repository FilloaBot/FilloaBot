import random, time, json, asyncio
import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot

from cogs.filloas import Filloas
from cogs.admin_tools import *
from cogs.events import Events

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



"""
@bot.listen()
async def on_message(message):
    if message.author == bot.user:
        return
    references = json.load(open("config/references.json"))["references"]
    for reference in references:
        if references.search(reference["regex"], message.content) != None:
            await message.channel.send(reference["answer"])
            for reaction in reference["reactions"]:
                await message.add_reaction(reaction)
            await bot.process_commands(message)
"""

bot.run(token)