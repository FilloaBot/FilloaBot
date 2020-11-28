import youtube_dl 
import os

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
        
        if not voice == None:
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

        await ctx.guild.change_voice_state(channel=channel, self_deaf=True)
        
    @commands.command()
    async def leave(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild = ctx.guild)

        if not voice == None:
            await voice.disconnect()
            await ctx.send(f"Desconectado del canal {channel}")
        else:
            await ctx.send("No estoy conectado a ningun canal fetido")

    @commands.command()
    async def play(self, ctx, url: str):
        if ctx.author.voice == None:
            await ctx.send("No estas en un canal de voz melon")
            return
        
        msgSplit = ctx.message.content.split(" ")
        if len(msgSplit) > 2:
            msgSplit.pop(0)
            url = " ".join(msgSplit)

        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild = ctx.guild)

        if not voice == None:
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

        await ctx.guild.change_voice_state(channel = channel, self_deaf = True)

        await ctx.send("Comenzando descarga...")

        filePath = str(ctx.guild.id) + ".mp3"

        if os.path.exists(filePath):
            os.remove(filePath)

        ydl_opts = {
            'default_search': 'auto',
            'outtmpl': filePath,
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        await ctx.send(f"Descarga finalizada. Reproduciendo `{url}`.")

        player = FFmpegPCMAudio(filePath)
        if voice.is_playing():
            voice.stop()
        
        voice.play(player)
        
    @commands.command()
    async def pause(self, ctx):
        voice = get(self.bot.voice_clients, guild = ctx.guild)

        if voice and voice.is_playing():
            voice.pause()
            await ctx.send("Pausando reproduccion")
        else:
            await ctx.send("No estas reproduciendo nada ahora mismo")
            
    @commands.command()
    async def resume(self, ctx):
        voice = get(self.bot.voice_clients, guild = ctx.guild)

        if voice and voice.is_paused():
            voice.resume()
            await ctx.send("Resumiendo reproduccion")
        else:
            await ctx.send("Ya se esta reproduciendo, no se puede resumir melon")

    @commands.command()
    async def stop(self, ctx):
        voice = get(self.bot.voice_clients, guild = ctx.guild)

        if voice and voice.is_playing():
            voice.stop()
            await ctx.send("Parando de reproducir")
        else:
            await ctx.send("La reproduccion ya esta parada melon")