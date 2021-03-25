import random
from typing import Optional
from discord import Color

import discord
from discord import Embed, Member
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType, BadArgument

from cogs.utils.database import *

database = main_db("./database.db")
emoji = "<:filoacoin:811229504692420608>"

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @cooldown(1, 30, BucketType.user)
    async def farm(self, ctx):
        #print(f"{ctx.author} ha intentado farmear dinero")
        user = str(ctx.author)
        money = random.randint(200, 600)
        database.add_user_balance(user, money)

        await ctx.send(f"Has farmeado esta cantidad de dinero `{money}` {emoji}")

    @commands.command()
    async def balance(self, ctx, user: Optional[Member]):

        user = user or ctx.message.author
        userStr = str(user)
        embed = Embed(
            title = f"Balance económico [{user.name}]",
            colour = Color(0xFFFFFF)
        )

        if not database.user_exist(userStr):
            await ctx.send("El usuario no existe")
            return 
                
        money = str(database.get_user_balance(userStr))
        bank = str(database.get_user_bank(userStr))

        embed.add_field(name = "_**Cartera**_", value = f"El dinero actual en la cartera de {user.mention} es: **{money}** {emoji}")
        embed.add_field(name = "_**Banco**_", value = f"El dinero actual en el banco de {user.mention} es : **{bank}** {emoji}")

        await ctx.send(embed = embed)

    @balance.error
    async def balance_error(self, ctx, exc):
        if isinstance(exc, BadArgument):
            await ctx.send("El usuario no existe melon")

    @commands.command()
    @cooldown(1, 60, BucketType.user)
    async def steal(self, ctx, target: Optional[Member]):
        if target == None:
            await ctx.send("Tienes que poner al usuario al que quieres robar fetido")
            return

        targetStr = str(target)
        userStr = str(ctx.message.author)
        current_balance = database.get_user_balance(userStr)
        target_balance = database.get_user_balance(targetStr)
        if current_balance < 500 or current_balance == None:
           await ctx.send(f"No puedes robar dinero hasta que tengas mas de 500 {emoji} manin")
           return
        if target_balance == 0 or target_balance == None:
            await ctx.send(f"{target.mention} ya está seco")
            return

        probabilidad = random.randint(1, 8)#1/2 of probability to steal, 1/8 to pay and 3/8 to nothing
        if probabilidad <= 4:
            money_to_substract = random.randint(1, target_balance)
            database.exchange_balance(targetStr, userStr, money_to_substract)
            await ctx.send(f"Has robado con exito `{money_to_substract}` {emoji} de {target.mention}!")
        elif probabilidad == 5:
            money_to_substract = random.randint(1, 500)
            database.exchange_balance(userStr, targetStr, money_to_substract)
            await ctx.send(f"Te han pillado al robar :(\nPagas una multa de `{money_to_substract}` {emoji} a {target.mention}")
        else:
            await ctx.send(f"Te han pillado al robar :(\nPero {target.mention} te perdona y no pagas multa.")

        return

    @commands.command()
    @cooldown(1, 10, BucketType.user)
    async def give(self, ctx, target: Member, cantidad):
        if target == None:
            await ctx.send("Tienes que poner a quien vas a darle la pasta crack")
            return

        if type(cantidad) == int and cantidad == 0:
            await ctx.send("Tienes que poner la cantidad dinero que quieres dar manin")
            return
        
        targetStr = str(target)
        userStr  = str(ctx.message.author)
        current_balance = database.get_user_balance(userStr)

        if current_balance == 0:
            await ctx.send("No tienes dinero para dar crack")
            return None

        if cantidad == "all" or cantidad == "ALL":
            cantidad = database.get_user_balance(userStr)

        database.exchange_balance(userStr, targetStr, cantidad)
        await ctx.send(f"Le has dado al usuario {target.mention} `{cantidad}` {emoji} de monedas. Joder, ni que fueras bolsonaro")

        return 0

    @commands.command()
    async def deposit(self, ctx, cantidad):
        if cantidad == None:
            await ctx.send("Introduce una canditad")
            return
        if type(cantidad) == int and cantidad == 0:
            await ctx.send("Pon un valor correcto")
            return                                  
                                                        
        userStr = str(ctx.author)
        current_user_balance = database.get_user_balance(userStr)                                                
         
        if int(current_user_balance) == 0:                     
            await ctx.send("No tienes pasta manin")
            return

        if int(current_user_balance) < int(cantidad):
            await ctx.send("No puedes depositar mas del dinero que tienes fiera")
            return

        if int(cantidad) < 0:
            await ctx.send("Que intentas manin")
            return                                         
                                                              
        if str(cantidad.lower()) == 'all': 
            cantidad = database.get_user_balance(userStr)
            database.deposit(userStr, cantidad)
            await ctx.send(f"Depositaste `{current_user_balance}` en tu cuenta")

        else:                   
            database.deposit(userStr, int(cantidad))
            await ctx.send(f"Depositaste `{cantidad}` {emoji} en tu cuenta")

    @commands.command()
    async def withdraw(self, ctx, cantidad):
        if cantidad == None:
            await ctx.send("Introduce una canditad")
            return
        if type(cantidad) == int and cantidad == 0:
            await ctx.send("Pon un valor correcto")
            return                                  
                                                        
        userStr = str(ctx.author)           
        current_bank_balance = int(database.get_user_bank(userStr))
        
        if int(current_bank_balance) < int(cantidad):
            await ctx.send("No pudes sacar mas del dinero que tienes fiera")
            return
        
        else:
            pass

        if int(cantidad) < 0:
            await ctx.send("Que intentas manin")
            return
         
        if int(current_bank_balance) == 0:                     
            await ctx.send("No tienes pasta manin")
            return                                        

        if str(cantidad.lower()) == 'all': 
            cantidad = database.get_user_bank(userStr)
            database.withdraw(userStr, cantidad)
            await ctx.send(f"Sacaste `{current_bank_balance}` de tu cuenta")
        else:                   
            database.withdraw(userStr, int(cantidad))
            await ctx.send(f"Sacaste `{cantidad}` {emoji} de tu cuenta") 

def setup(bot):
    bot.add_cog(Economy(bot))