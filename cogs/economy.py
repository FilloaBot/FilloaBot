import random
from typing import Optional

import discord
from discord.ext import commands
from discord import Embed, Member

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

    @commands.command()
    async def balance(self, ctx, user: Optional[Member]):
        target = user or ctx.author
        embed = Embed(
            tittle = "Tu balance economico actual",
            colour = target.colour
        )
        
        user = str(user) or str(ctx.author)
        if not database.user_exist(user):
            await ctx.send("El usuario no existe")
        money = str(database.get_user_balance(user))

        embed.set_footer(text = f"Tu dinero actual es: {money}")

        await ctx.send(embed = embed)

    @commands.command()
    async def steal(self, ctx):
        pass
    