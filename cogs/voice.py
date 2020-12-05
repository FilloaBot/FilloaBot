import youtube_dl 
import os
import shutil


import discord
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio, Embed, Color

from cogs.utils.database import *

database = main_db("./database.db")

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
    async def play(self, ctx, url: str, noQueue="f"):
        if not noQueue == True:
            noQueue = False
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

        ydl_opts = {
            'default_search': 'auto'
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            try:
                info_dict = info_dict["entries"][0]
            except Exception as e:
                pass
            video_id = info_dict.get("id", None)
            video_url = "https://youtube.com/watch?v=" + video_id
            video_title = info_dict.get('title', None)
        if not noQueue:
            database.insert_into_queue(ctx.guild.id, video_id)
        url = video_id

        if voice == None or not voice.is_playing():
            filePath = str(ctx.guild.id) + ".mp3"
            if os.path.exists(filePath):
                os.remove(filePath)
            ydl_opts = {
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
        else:
            embed = Embed(
                title = "**Añadido a la cola**",
                description = f"[{video_title}]({video_url}) [{ctx.message.author.mention}]",
                colour = Color(0x3A425D),
            )
            await ctx.send(embed = embed)
        
    @commands.command()
    async def queue(self, ctx):
        ydl_opts = {
            'default_search': 'auto'
        }

        videos = []
        queue = database.get_queue(ctx.guild.id)
        if queue == None:
            embed = Embed(
                title = "**Cola vacía**",
                colour = Color(0x3A425D),
            )
            await ctx.send(embed=embed)
        for ytId in queue["queue"]:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(ytId, download=False)
                video_id = info_dict.get("id", None)
                video_url = "https://youtube.com/watch?v=" + video_id
                video_title = info_dict.get('title', None)
            dict = {
                "name": video_title,
                "url": video_url
            }
            videos.append(dict)

        embed = Embed(
            title = f"Cola de reproducción",
            colour = Color(0x3A425D)
        )

        currentPos = database.get_queue(ctx.guild.id)["currentPos"]
        i=0
        for video in videos:
            video_title = video["name"]
            video_url = video["url"]
            current = ""
            if i == currentPos:
                current = "_[Reproduciendo]_"
            embed.add_field(name = f"**{str(i)} {current}**", value = f"[{video_title}]({video_url})")
            
            i +=1
        await ctx.send(embed = embed)
            



    @commands.command()
    async def next(self, ctx):
        emoji = '⏭️'
        msg = ctx.message
        await msg.add_reaction(emoji)
        voice = get(self.bot.voice_clients, guild = ctx.guild)
 
        nextYtId = database.get_queue(ctx.guild.id)["queue"][database.increment_current_pos(ctx.guild.id)]
        pending_command = self.bot.get_command("play")
        if not voice == None:
            voice.stop()
        await ctx.invoke(pending_command, nextYtId, True)

    @commands.command()
    async def previous(self, ctx):
        emoji = '⏮️'
        msg = ctx.message
        await msg.add_reaction(emoji)
        voice = get(self.bot.voice_clients, guild = ctx.guild)
 
        nextYtId = database.get_queue(ctx.guild.id)["queue"][database.decrement_current_pos(ctx.guild.id)]
        pending_command = self.bot.get_command("play")
        if not voice == None:
            voice.stop()
        await ctx.invoke(pending_command, nextYtId, True)

    @commands.command()
    async def clear(self, ctx):
        emoji = '⬜'
        msg = ctx.message
        await msg.add_reaction(emoji)
        voice = get(self.bot.voice_clients, guild = ctx.guild)
 
        database.clear_queue(ctx.guild.id)
        if not voice == None:
            voice.stop()
        embed = Embed(
                title = "**Cola vaciada**",
                colour = Color(0x3A425D),
            )
        await ctx.send(embed=embed)
            
    @commands.command()
    async def resume(self, ctx):
        emoji = '▶️'
        msg = ctx.message
        await msg.add_reaction(emoji)

        voice = get(self.bot.voice_clients, guild = ctx.guild)

        if not voice == None and voice.is_paused():
                voice.resume()
    @commands.command()
    async def stop(self, ctx):
        emoji = '🛑'
        msg = ctx.message
        await msg.add_reaction(emoji)

        voice = get(self.bot.voice_clients, guild = ctx.guild)

        if not voice == None:
            voice.stop()
        