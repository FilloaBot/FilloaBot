import random 

from typing import Optional
from datetime import datetime

import discord
from discord import Embed, Member
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

    @commands.command(pass_context = True)
    async def user_info(self, ctx, target: Optional[Member]):
        target = target or ctx.message.author

        embed = Embed(
            title = "Informacion del usuario",
            description = f"Puedes ver como de gay es {target.mention} con `?gay`",
            colour = target.colour,
            timestamp = datetime.utcnow()
        )
        embed.set_thumbnail(url = target.avatar_url)
        await ctx.send(embed = embed)

    @commands.command(name = "help")
    async def help(self, ctx):
        # we are developing the filloabot website so there you will be able to see all the commands
        pass


def setup(bot):
    bot.add_cog(Admin_tools(bot))