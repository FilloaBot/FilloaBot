import random
import discord
from discord.ext import commands

class Filloas(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        pass_context = True
    )
    async def aleatorio(self, ctx, num1: int, num2: int):
        try:
            num = random.randint(num1, num2)
            await ctx.send("El numero aleatorio es: " + str(num))
        except ValueError:
            await ctx.send("Inserta un intervalo valido fetido")
            return

    #Only for testing purpouses, this wont be a real command
    @commands.command(name = "crear-canal")
    @commands.has_permissions(administrator = True)
    async def create_channel(self, ctx, channel_name):
        try:
            guild = ctx.guild
            existing_channel = discord.utils.get(guild.channels, name = channel_name)
            if not existing_channel:
                print(f"Creando nuevo canal: {channel_name}")
                await guild.create_text_channel(channel_name)
        except Exception:
            await ctx.send("No has usado el comando de forma correcta o no tienes permisos")
            return