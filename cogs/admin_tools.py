import random 
import discord
from discord.ext import commands

class Admin_tools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    #Only for testing purpouses, this wont be a real command
    @commands.command(name = "crear-canal")
    @commands.has_permissions(administrator = True)
    async def create_channel(self, ctx, channel_name):
        number = random.randint(0, 1)
        msg = ctx.message
        emoji = ["👍", "👌"]

        await msg.add_reaction(emoji[number])

        guild = ctx.guild
        existing_channel = discord.utils.get(guild.channels, name = channel_name)
        if not existing_channel:
            print(f"Creando nuevo canal: {channel_name}")
            await guild.create_text_channel(channel_name)