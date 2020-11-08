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
