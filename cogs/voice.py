import youtube_dl 
import os
import shutil
import random
import asyncio
from typing import Optional

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
    async def play(self, ctx, url: Optional[str], noQueue="False"):#No queue's default is a string for allowing various words in arguments
        if url == None:
            pending_command = self.bot.get_command("resume")
            await ctx.invoke(pending_command)
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
            try:
                info_dict = ydl.extract_info(url, download=False)
            except (youtube_dl.utils.DownloadError):
                embed = Embed(
                    title = "**No se han encotrado resultados**",
                    description = f"No hay resultados para **{url}**",
                    colour = Color(0xFF0000),
                    ) 
                await ctx.send(embed = embed)
                return
            try:
                info_dict = info_dict["entries"][0]
            except (KeyError, IndexError):
                pass
            video_id = info_dict.get("id", None)
            video_url = "https://youtube.com/watch?v=" + video_id
            video_title = info_dict.get('title', None)
            if video_title == None:
                embed = Embed(
                    title = "**No se han encotrado resultados**",
                    description = f"No hay resultados para **{url}**",
                    colour = Color(0xFF0000),
                    ) 
                await ctx.send(embed = embed)
                return
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
            database.modify_queue(ctx.guild.id, currentPos=database.get_queue(ctx.guild.id)["queue"].index(url))    
            embed = Embed(
                title = "**Reproduciendo**",
                description = f"[{video_title}]({video_url}) [{ctx.message.author.mention}]",
                colour = Color(0x3A425D),
            )
            await ctx.send(embed = embed)
            player = FFmpegPCMAudio(filePath)
            if voice.is_playing():
                voice.stop()
            def callback(error):
                if error != None:
                    raise error
                elif not noQueue:
                    
                    nonlocal ctx
                    pending_command = self.bot.get_command("next")
                    self.bot.loop.create_task(ctx.invoke(pending_command, True))
            voice.play(player, after=callback)
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
            return
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
        i = 0
        for video in videos:
            video_title = video["name"]
            video_url = video["url"]
            current = ""
            if i == currentPos:
                current = "_[Reproduciendo]_"
            embed.add_field(name = f"**{str(i + 1)} {current}**", value = f"[{video_title}]({video_url})")
            
            i +=1
        if queue["shuffle"]:
            embed.set_footer(text = "Reproducción mezclada activada")
        else: 
            embed.set_footer(text = "Reproducción mezclada desactivada")
        await ctx.send(embed = embed)

    @commands.command()
    async def next(self, ctx, isAutomatedCall=False):
        emoji = '⏭️'
        msg = ctx.message
        if not isAutomatedCall == True:
            isAutomatedCall = False
        if not isAutomatedCall:
            await msg.add_reaction(emoji)
        voice = get(self.bot.voice_clients, guild = ctx.guild)

        data = database.get_queue(ctx.guild.id)
        queue = data["queue"]
        pos = data["currentPos"]
        if data["shuffle"]:
            while pos == data["currentPos"]:
                pos = random.randint(0, len(queue)-1)
            # database.modify_queue(ctx.guild.id, currentPos=pos)
        else:
            pos += 1#database.increment_current_pos(ctx.guild.id)
        if pos >= len(queue):
            pos=0
        if pos < 0:
            pos= len(queue) - 1
        nextYtId = queue[pos]
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
        data = database.get_queue(ctx.guild.id)
        queue = data["queue"]
        pos = data["currentPos"]
        if data["shuffle"]:
            while pos == data["currentPos"]:
                pos = random.randint(0, len(queue)-1)
            # database.modify_queue(ctx.guild.id, currentPos=pos)
        else:
            pos -= 1#database.decrement_current_pos(ctx.guild.id)
        if pos >= len(queue):
            pos=0
        if pos < 0:
            pos= len(queue) - 1
        nextYtId = queue[pos]
        pending_command = self.bot.get_command("play")
        if not voice == None:
            voice.stop()
        await ctx.invoke(pending_command, nextYtId, True)

    @commands.command()
    async def shuffle(self, ctx):
        emoji = '🔀'
        msg = ctx.message
        await msg.add_reaction(emoji)
        data = database.get_queue(ctx.guild.id)
        shuffle = not data["shuffle"]
        database.modify_queue(ctx.guild.id, shuffle=shuffle)
        if shuffle:
            shuffleStr = "Activada"
        else:
            shuffleStr = "Desactivada"
        embed = Embed(
                title = f"Reproducción mezclada: **{shuffleStr}**",
                colour = Color(0x3A425D),
            )
        await ctx.send(embed=embed)

    @commands.command()
    async def remove(self, ctx, delPos: int):
        emoji = '❌'
        msg = ctx.message
        await msg.add_reaction(emoji)
        data = database.get_queue(ctx.guild.id)
        queue = data["queue"]
        delPos = delPos -1
        if delPos == data["currentPos"]:
            database.modify_queue(ctx.guild.id, currentPos=0)
        if delPos < 0 or delPos >= len(queue):
            embed = Embed(
                title = "**Ese número no esta en la cola**",
                colour = Color(0xFF0000),
            )
            await ctx.send(embed=embed)
            return
        ydl_opts = {
            'default_search': 'auto'
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ytId = queue[delPos]
            info_dict = ydl.extract_info(ytId, download=False)
            video_id = info_dict.get("id", None)
            video_url = "https://youtube.com/watch?v=" + video_id
            video_title = info_dict.get('title', None)
        database.remove_from_queue(ctx.guild.id, delPos)
        embed = Embed(
                title = "**Borrado de la cola**",
                description = f"Borrado [{video_title}]({video_url})",
                colour = Color(0x3A425D),
            )
        await ctx.send(embed=embed)

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
    async def pause(self, ctx):
        emoji = '⏸️'
        msg = ctx.message
        await msg.add_reaction(emoji)

        voice = get(self.bot.voice_clients, guild = ctx.guild)

        if not voice == None and voice.is_playing():
                voice.pause()

    @commands.command()
    async def stop(self, ctx):
        emoji = '🛑'
        msg = ctx.message
        await msg.add_reaction(emoji)

        voice = get(self.bot.voice_clients, guild = ctx.guild)

        if not voice == None:
            voice.stop()
        