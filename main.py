import json
import asyncio
import discord
import random, time
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from config.variables import *

#load the bot toke from the json file
with open("token.json") as file:
    data = json.load(file)
token = data['token']

intents = discord.Intents.default()
intents.members = True
intents.reactions = True
intents.messages = True
intents.emojis = True
bot = commands.Bot(command_prefix = '?', description = "Bot para diversos propositos")

@tasks.loop(seconds=25)
async def comprobar_pechi():
    channel = await bot.get_channel(channel.user.id) 
    await channel.send("A pechi le gusta oliveira")

@bot.command(
    name = "filloas",
    description = "Mustra fotos de filloas",
    brief = "Muestra fotos de filloas aleatorioas, por lo demas, no sirve para nada",
    pass_context = True
)
async def filloas(ctx):
    number = random.randint(0, 2)
    await ctx.send(urls[number])

@bot.command(
    name = "aleatorio",
    description = "Genera un numero aleatorio en un intervalo dado",
    brief = "Genera un numero aleatorio en un intervalo dado",
    pass_context = True
)
async def aleatorio(ctx, num1: int, num2: int):
    number = random.randint(num1, num2)
    await ctx.send(number)

@bot.command(
    name = "twitch",
    description = "Muestra mi canal de twitch",
    brief = "Pone mi canal de twitch al que te puedes suscribir gratis si tienes amazon prime <3",
    pass_context = True
)
async def twitch(ctx):
    await ctx.send("Visita mi canal de twitch: " + urls[3])



@bot.event
async def on_ready():
    game = discord.Game("Usa ? para invocar al filloa bot")
    await bot.change_presence(status = discord.Status.idle, activity = game)
    print("Filloa bot encendio")
    print("\nLogged in as")
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.listen()
async def on_message(message):
    if message.content.endswith("5"):        
        await message.channel.send("Por el culo te la inco")
        await bot.process_commands(message)

bot.run(token)