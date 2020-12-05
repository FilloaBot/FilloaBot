import random
from typing import Optional
from discord import Color

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
        user = user or ctx.message.author
        user = str(user)
        embed = Embed(
            title = "Balance económico",
            colour = Color(0xFFFFFF)
        )

        if not database.user_exist(user):
            await ctx.send("El usuario no existe")
            return 
            
        money = str(database.get_user_balance(user))

        embed.add_field(name = "_**Cartera**_", value = f"Tu dinero actual en la cartera es: **{money}**")

        await ctx.send(embed = embed)

    @commands.command()
    async def steal(self, ctx, target: Optional[Member]):
        if target == None:
            await ctx.send("Tienes que poner al usuario al que quieres robar fetido")
            return None
    
        user = str(ctx.author)
        current_balance = database.get_user_balance(user)
        if current_balance < 500:
           await ctx.send("No puedes robar dinero hasta que tengas mas de 500 monedas manin")

        probabilidad = random.randint(1, 8)
        if probabilidad == 1:
            database.substract_balance(target, int((current_balance+500)/current_balance))
            susbtracted_money = int((current_balance+500)/current_balance)
            await ctx.send(f"Has robado con exito {susbtracted_money}!")
        else:
            await ctx.send("No has podido robar :(")

        return