import discord
from discord.utils import get
import aiohttp
import glob
import random
from random import randrange
import time
import requests
import os
from discord.ext import commands

#auth
TOKEN = os.environ['TOKEN']

MSG_HELP = "pong        Response ping\r" \
           "cat         Post a random cat pic\r"

client = discord.Client()
bot = commands.Bot(command_prefix='/', help_command=None)

__games__ = []
voice_channel = ""


def __get_gif__(key_word):
    rand_num = randrange(10)
    key_word = key_word.replace(' ', '-')
    url = 'https://api.tenor.com/v1/search?q='+key_word+'&limit='+str(rand_num)
    x = requests.get(url)
    if x.status_code == 200:
        return x.json()['results'][rand_num-1]['url']
    else:
        return ''


@bot.command()
async def ping(ctx):
    await ctx.send('pong')


@bot.command()
async def help(ctx):
    await ctx.send(MSG_HELP)


@bot.command()
async def cat(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get('http://aws.random.cat/meow') as r:
            if r.status == 200:
                js = await r.json()
                await ctx.send(js['file'])


bot.run(TOKEN)
