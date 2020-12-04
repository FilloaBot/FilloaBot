import youtube_dl 
import os
import shutil


import discord
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio, Embed, Color

queues = {}

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
            info_dict = ydl.extract_info(url, download=False)
            info_dict = info_dict["entries"][0]
            video_id = info_dict.get("id", None)
            video_url = "https://youtube.com/watch?v=" + video_id
            video_title = info_dict.get('title', None)

        embed = Embed(
            title = "**Reproduciendo**",
            description = f"[{video_title}]({video_url}) [{ctx.message.author.mention}]",
            colour = Color(0x3A425D),
        )
        await ctx.send(embed = embed)

        player = FFmpegPCMAudio(filePath)
        if voice.is_playing():
            voice.stop()
        
        voice.play(player)
        
    @commands.command()
    async def pause(self, ctx):
        emoji = '⏸️'
        msg = ctx.message
        await msg.add_reaction(emoji)

        voice = get(self.bot.voice_clients, guild = ctx.guild)

        if voice and voice.is_playing():
            voice.pause()
        #     await ctx.send("Pausando reproduccion")
        # else:
        #     await ctx.send("No estas reproduciendo nada ahora mismo")
            
    @commands.command()
    async def resume(self, ctx):
        emoji = '▶️'
        msg = ctx.message
        await msg.add_reaction(emoji)

        voice = get(self.bot.voice_clients, guild = ctx.guild)

        if not voice == None:
            if voice.is_paused():
                voice.resume()
        #         await ctx.send("Resumiendo reproduccion")
        #     elif voice.is_playing():
        #         await ctx.send("Ya se esta reproduciendo, no se puede resumir melon")
        #     else:
        #         await ctx.send("No se esta reproduciendo nada, no se puede resumir melon")
        # else:
        #     await ctx.send("No se esta reproduciendo nada, no se puede resumir melon")

    @commands.command()
    async def stop(self, ctx):
        emoji = '🛑'
        msg = ctx.message
        await msg.add_reaction(emoji)

        voice = get(self.bot.voice_clients, guild = ctx.guild)

        if not voice == None:
            # await ctx.send("Parando de reproducir")
            voice.stop()
        # else:
        #     await ctx.send("No se esta reproduciendo nada, no se puede parar melon")

    @commands.command()
    async def queue(self, ctx, url: str):
        Queue_infile = os.path.isdir("./Queue")

        if Queue_infile is False:
            os.mkdir("Queue")

        DIR = os.path.abspath(os.path.realpath("Queue"))
        q_num = len(os.listdir(DIR))
        q_num += 1
        add_queue = True
        while add_queue:
            if q_num in queues:
                q_num += 1
            else:
                add_queue = False
                queues[q_num] = q_num
        
        queue_path = os.path.abspath(os.path.realpath("Queue"))

        ydl_opts = {
            'default_search': 'auto',
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        await ctx.send(f"Añadiendo la cancion {str(q_num)} a la cola")