import json
import discord
from discord.ext import commands
import random

from config.variables import *

#load the bot toke from the json file
with open("token.json") as file:
    data = json.load(file)

token = data['token']

bot = commands.Bot(command_prefix = '?', description = "Bot para diversos propositos")

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

@bot.listen()
async def on_message(message):
    if message.content.endswith("5"):
        await message.channel.send("Por el culo te la inco")
        await bot.process_commands(message)

bot.run(token)