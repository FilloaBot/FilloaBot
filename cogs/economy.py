import random
from typing import Optional
from colour import Color

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
        embed = Embed(
            tittle = "Tu balance economico actual",
            colour = Color(0xFFFFFF)
        )

        if not database.user_exist(user):
            await ctx.send("El usuario no existe")
            return 
            
        money = str(database.get_user_balance(str(user)))

        embed.set_footer(text = f"Tu dinero actual es: {money}")

        await ctx.send(embed = embed)

    @commands.command()
    async def steal(self, ctx):
        pass
    