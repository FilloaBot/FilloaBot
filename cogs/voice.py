import discord
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio

class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def join(self, ctx):
        global voice
        if ctx.message.author.voice == None:
            await ctx.send("No estas en un canal de voz melon.")
            return 
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild = ctx.guild)
        
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

        await ctx.guild.change_voice_state(channel=channel, self_deaf=True)
        player = FFmpegPCMAudio("fuentedepoder.mp3")
        voice.play(player)

    @commands.command()
    async def leave(self, ctx):
        channel = ctx.message.voice.channel
        voice = get(self.bot.voice_clients, guild = ctx.guild)

        if voice and voice.is_connected():
            await voice.disconnect()
            await ctx.send(f"Desconectado del canal {channel}")
        else:
            await ctx.send("No estoy conectado a ningun canal fetido")

    @commands.command()
    async def play(self, ctx, url: str):
        if ctx.author.voice == None:
            await ctx.send("No estas en un canal de voz melon")
            return

        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild = ctx)
        
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await voice.connect()