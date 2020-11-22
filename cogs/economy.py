import random
import discord
from discord.ext import commands



class Economy(commands.Cog):
    """
    The economy is going to be one of the main purposes of this bot
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        pass_context = True
    )
    async def farm(self, ctx):
        money = random.randint(200, 600)
        await ctx.send(f"Has farmeado esta cantidad de dinero `{money}`")

    @commands.command(
        pass_context = True
    )
    async def banco(self, ctx, operation):
        pass

    @commands.command()
    async def balance(self, ctx):
        pass

    @commands.command()
    async def steal(self, ctx, user):
        pass
    