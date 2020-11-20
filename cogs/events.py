import json
import re
from itertools import cycle
import discord
from discord.ext import commands, tasks
from discord.utils import get

from cogs.config.variables import status

status = cycle(status)

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(seconds = 3600)
    async def change_status(self):
        await self.bot.change_presence(activity = discord.Game(next(status)))
        print("LOG: status changed")

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
        if message.author == self.bot.user:
            return
        references = json.load(open("cogs/config/references.json"))["references"]
        for reference in references:
            if re.search(reference["regex"], message.content.lower()) != None:
                await message.channel.send(reference["answer"])
                for reaction in reference["reactions"]:
                    await message.add_reaction(reaction)
                await self.bot.process_commands(message)   