import random, time, json, asyncio
import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from itertools import cycle

from config.variables import *
from cogs.greeting import *
from cogs.filloas import *

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

status = cycle(status)

bot.add_cog(Greeting(bot))
bot.add_cog(Filloas(bot))

#Comandos
@bot.command(
    name = "filloas",
    description = "Mustra fotos de filloas",
    brief = "Muestra fotos de filloas aleatorioas, por lo demas, no sirve para nada",
    pass_context = True
)
async def filloas(ctx):
    number = random.randint(0, 3)
    await ctx.send(urls[number])

#Tasks
@tasks.loop(seconds = 10)
async def change_status():
    await bot.change_presence(activity = discord.Game(next(status)))
    print("LOG: status changed")

#Eventos
@bot.event
async def on_ready():

    change_status.start()
    print("Filloa bot encendio")
    print("\nLogged in as")
    print(bot.user.name)
    print(bot.user.id)
    print('------')

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