import requests
import json
import re
from itertools import cycle
import discord
from discord.ext import commands, tasks
from discord.utils import get
from discord.ext.commands import (
    BadArgument,
    CommandNotFound,
    MissingRequiredArgument,
    CommandOnCooldown
)

from cogs.config.variables import status

status = cycle(status)

IGNORE_EXCEPTIONS = (BadArgument)

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(seconds = 3600)
    async def change_status(self):
        await self.bot.change_presence(activity = discord.Game(next(status)))
        #print("LOG: status changed")

    @commands.Cog.listener()
    async def on_ready(self):
        self.change_status.start()
        print("Filloa bot encendio")
        print("\nLogged in as")
        print(self.bot.user.name)
        print(self.bot.user.id)
        print('------')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send("Bienvenido {0.mention}".format(member))

        role = get(member.guild.roles, name = "Filloador")
        await member.add_roles(role)
        print(f"{member} has been given {role}")


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user or not self.bot.get_command(message.content.split(" ")[0][1:]) == None:
            return
        references = json.load(open("cogs/config/references.json"))["references"]
        for reference in references:
            if re.search(reference["regex"], message.content.lower()) != None:
                if re.search("^https?://.*\..*$", reference["answer"]):

                    url = reference["answer"]
                    fileName = "cache/" + url[url.rindex("/")+1:]
                    r = requests.get(url)
                    with open(fileName, 'wb') as f:
                        f.write(r.content) 
                    await message.channel.send(file=discord.File(fileName))
                else:
                    await message.channel.send(reference["answer"])
                for reaction in reference["reactions"]:
                    await message.add_reaction(reaction)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, exc):
        if isinstance(exc, CommandOnCooldown):
            await ctx.send(f"El comando esta en cooldown, intentalo de nuevo en `{exc.retry_after:,.2f}` segundos. MELON")

        elif isinstance(exc, CommandNotFound):
            await ctx.send("Ese comando no existe papafilloas :middle_finger:")

def setup(bot):
    bot.add_cog(Events(bot))