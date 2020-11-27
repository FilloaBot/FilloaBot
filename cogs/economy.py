import random
import discord
from discord.ext import commands
from discord.utils import get

from cogs.utils.database import *

database = main_db("./database.db")

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        pass_context = True
    )
    async def farm(self, ctx):
        user = str(ctx.author)

        money = random.randint(200, 600)
        database.add_user_balance(user, money)
        
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
    