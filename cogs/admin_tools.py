import discord
from discord.ext import commands

def get_user(message, user):
    try:
        member = message.mentions[0]
    except:
        member = message.guild.get_member_named(user)
    if not member:
        try:
            member = message.guild.get_member(int(user))
        except ValueError:
            pass
    if not member:
        return None
    return member

class Admin_tools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def are_overwrites_empty(self, overwrites):
        """There is currently no cleaner way to check if a
        PermissionOverwrite object is empty"""
        original = [p for p in iter(overwrites)]
        empty = [p for p in iter(discord.PermissionOverwrite())]
        return original == empty
    
     #Only for testing purpouses, this wont be a real command
    @commands.command(name = "crear-canal")
    @commands.has_permissions(administrator = True)
    async def create_channel(self, ctx, channel_name):
        guild = ctx.guild
        existing_channel = discord.utils.get(guild.channels, name = channel_name)
        if not existing_channel:
            print(f"Creando nuevo canal: {channel_name}")
            await guild.create_text_channel(channel_name)

    @commands.command(pass_context=True)
    async def kick(self, ctx, user, *, reason = ""):
        """Kicks a user (if you have the permission)."""
        user = get_user(ctx.message, user)
        if user:
            try:
                await user.kick(reason=reason)
                return_msg = "Kicked user `{}`".format(user.mention)
                if reason:
                    return_msg += " for reason `{}`".format(reason)
                return_msg += "."
                await ctx.message.edit(content = self.bot.bot_prefix + return_msg)
            except discord.Forbidden:
                await ctx.message.edit(content = self.bot.bot_prefix + 'Could not kick user. Not enough permissions.')
        else:
            return await ctx.message.edit(content = self.bot.bot_prefix + 'Could not find user.')