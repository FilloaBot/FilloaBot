import random
import discord
from discord.ext import commands

from cogs.config.variables import urls

class Filloas(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

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

    @commands.command()
    async def hello(self, ctx, *, member: discord.member = None):
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send("Hola {0.name}".format(member))
        else:
            await ctx.send("Hola de nuevo {0.name}".format(member))
        self._last_member = member

    @commands.command(
        name = "filloas",
        description = "Mustra fotos de filloas",
        brief = "Muestra fotos de filloas aleatorioas, por lo demas, no sirve para nada",
        pass_context = True
    )
    async def filloas(self, ctx):
        number = random.randint(0, 3)
        await ctx.send(urls[number])

    @commands.command()
    async def gay(self, ctx, user):
        num = random.randint(0, 100)

        await ctx.send(f"El usuario {user} es {num}% homosexual")
