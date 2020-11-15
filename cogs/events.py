from itertools import cycle
import discord
from discord.ext import commands, tasks
from discord.utils import get

from config.variables import status

status = cycle(status)

@tasks.loop(seconds = 10)
async def change_status(self):
    await self.bot.change_presence(activity = discord.Game(next(status)))
    print("LOG: status changed")

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        change_status.start()
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

        