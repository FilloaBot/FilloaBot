import urllib
from bs4 import BeautifulSoup
import re

import discord
from discord.ext import commands
from discord import Embed, Color

class Ubports(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name = "ubports",
        description = "Muestra la cantidad de dispositivos compatibles con UbPorts actualmente.",
        brief = "Dispositivos compatibles con ubports actualmente",
        pass_context = True
    )
    async def ubports(self, ctx, extraShit="-"):
        url = "https://devices.ubuntu-touch.io/"
        request = urllib.request.Request(
            url,
            data=None, 
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            }
        )
        fullData = urllib.request.urlopen(request).read()
        soupData = BeautifulSoup(fullData, features="lxml")
        devicesCardText = str(soupData.find_all('p')[0])
        devicesInt = int(re.search('\d+', devicesCardText).group())
        embed = Embed(
                title = "¡Crea tu propio port de Ubuntu Touch!",
                description = f"Seguro, tres mil millones de dispositivos ejecutan Java. ¿Pero sabías que **{devicesInt}** dispositivos ejecutan [Ubuntu Touch](https://ubuntu-touch.io/)? Por cierto, si tu dispositivo no está entre estos, ¡Puede que estes interesado en aprender [cómo hacer el porteo número {devicesInt+1} de Ubuntu Touch!](http://docs.halium.org/en/latest/porting/first-steps.html)",
                colour = Color(0xCE4501)
        )
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Ubports(bot))