import discord
from discord.utils import get
import aiohttp
# import glob
import random
from random import randrange
# import time
import requests
import os
from discord.ext import commands

TOKEN = os.environ['TOKEN']

MSG_HELP = "```pong        Response ping\r" \
           "cat         Post a random cat pic```"

client = discord.Client()
bot = commands.Bot(command_prefix=('$'), help_command=None)

__games__ = []
voice_channel = ""
dct_enemie = {}


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


@bot.command()
async def join(ctx):
    vc = get(ctx.bot.voice_clients, guild=ctx.guild)
    if vc:
        await vc.disconnect()
    connected = ctx.author.voice
    if connected:
        await connected.channel.connect()


@bot.command()
async def leave(ctx):
    vc = get(ctx.bot.voice_clients, guild=ctx.guild)
    if vc:
        await vc.disconnect()


@bot.command()
async def roll(ctx, *args):

    n_dice = 1
    n_face = 2
    try:
        if len(args) == 0:
            pass
        elif len(args) == 1:
            n_dice = 1
            n_face = int(args[0])
        elif len(args) == 2:
            n_dice = int(args[0])
            n_face = int(args[1])
        else:
            raise Exception('Not enough arguments')

        msg = ''
        for i in range(0, n_dice):
            if n_face == 2:
                msg += random.choice([':white_check_mark:', ':x:'])+'       '
            else:
                msg += str(random.randrange(1, int(n_face)))+'      '

        await ctx.send(msg)

    except ValueError:
        await ctx.send('Arguments of poll need to be integers')
    except Exception as e:
        print(e.__class__.__name__)
        await ctx.send(e)


@bot.command()
async def dmg(ctx, enemie, damage, *args):
    if enemie not in dct_enemie:
        dct_enemie[enemie] = damage
        print(dct_enemie)
    elif damage == 'dead':
        dct_enemie[enemie] = 'dead'
    else:
        dct_enemie[enemie] = int(dct_enemie[enemie]) + int(damage)
        print(dct_enemie)

    if damage == 'dead':
        msg = enemie + ' mort'
    else:
        msg = damage + ' degat sur ' + enemie
    await ctx.send(msg)


@bot.command()
async def monsters(ctx):
    msg = '```'
    for i in dct_enemie:
        msg = msg + i + ' : ' + dct_enemie[i] + '\n'
    msg = msg + '```'
    await ctx.send(msg)


@bot.command()
async def clear(ctx):
    global dct_enemie
    dct_enemie = {}
    msg = 'table vider avec succes'
    await ctx.send(msg)


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching,
        name='$help'))
    print('Bot ready')

bot.run(TOKEN)
