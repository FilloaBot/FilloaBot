import sqlite3
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
        await ctx.send("Has farmeado esta cantidad de dinero")

    @commands.command(
        pass_context = True
    )
    async def banco(self, ctx):
        pass