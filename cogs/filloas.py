import random
import aiohttp
import json
from typing import Optional
import praw

import discord
# from discord import Bot
from discord.ext import commands
from discord import Embed, Member

from cogs.config.variables import urls

with open("cogs/config/reddit.json") as file:
    data = json.load(file)
    
token = data["reddit_token"]
secret_token = data["reddit_secret_token"]

class Filloas(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        # while not bot.is_ready():
        #     pass
        # self.invite = discord.utils.oauth_url(client_id=bot.user.id, permissions=discord.Permissions(37080128))
        self.inviteLink = None

        self.reddit = None
        if token and secret_token:
            self.reddit = praw.Reddit(
                client_id = token,
                client_secret = secret_token,
                user_name = "",
                password = "",
                user_agent = "FILLOA_BOT" 
            )

    @commands.command(
        pass_context = True
    )
    async def aleatorio(self, ctx, num1: int, num2: int):
        try:
            num = random.randint(num1, num2)
            await ctx.send("El numero aleatorio es: " + str(num))
        except ValueError:
            await ctx.send("Inserta un intervalo valido fetido")
            return

    @commands.command()
    async def hello(self, ctx, *, member: discord.member = None):
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send("Hola {0.name}".format(member))
        else:
            await ctx.send("Hola de nuevo {0.name}".format(member))
        self._last_member = member

    @commands.command(
        name = "filloas",
        description = "Mustra fotos de filloas",
        brief = "Muestra fotos de filloas aleatorioas, por lo demas, no sirve para nada",
        pass_context = True
    )
    async def filloas(self, ctx):
        number = random.randint(0, 3)
        await ctx.send(urls[number])

    @commands.command()
    async def gay(self, ctx, user: Optional[Member]):
        user = user.mention or ctx.message.author.mention
        num = random.randint(0, 100)

        await ctx.send(f"El usuario {user} es {num}% homosexual")

    @commands.command()
    async def ping(self, ctx):
        latency = self.bot.latency
        await ctx.send(f"La latencia del bot es: {latency * 1000} ms")
        
    @commands.command()
    async def invite(self, ctx):
        if self.inviteLink == None:
            self.inviteLink = discord.utils.oauth_url(client_id=self.bot.user.id, permissions=discord.Permissions(37080128))
        await ctx.send(f"Puedes invitar el bot aqui <{self.inviteLink}>")

    @commands.command(
        brief = "Show memes from reddit"
    )
    async def meme(self, ctx, subreddit="memes"):
        subreddit = self.reddit.subreddit(subreddit)
        all_submisions = []

        top = subreddit.top(limit = 50)

        for submission in top:
            all_submisions.append(submission)

        random_sub = random.choice(all_submisions)

        title = random_sub.title
        url = random_sub.url
        name = random_sub.name
        author = random_sub.author
        link = "https://www.reddit.com" + random_sub.permalink
        author_link = "https://www.reddit.com/user/" + author.name

        embed = Embed(
            title = title
        )
        embed.set_image(url = url)
        embed.set_footer(text = "Reddit",icon_url = "https://images-eu.ssl-images-amazon.com/images/I/418PuxYS63L.png")
        embed.set_author(name=f"Posted by u/{author}", url=link)

        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Filloas(bot))