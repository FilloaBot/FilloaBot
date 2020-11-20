import discord
from discord.ext import commands
from discord.utils import get

class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """
    Until we can download the discord.py[voice], this wont work
    """
    @commands.command()
    async def join(self, ctx):
        global voice
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild = ctx.guild)
        
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

        await voice.disconnect()

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()