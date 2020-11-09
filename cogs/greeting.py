import discord
from discord.ext import commands

class Greeting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send("Bienvenido {0.mention}".format(member))
        
    @commands.command()
    async def hello(self, ctx, *, member: discord.member = None):
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send("Hola {0.name}".format(member))
        else:
            await ctx.send("Hola de nuevo {0.name}".format(member))
        self._last_member = member