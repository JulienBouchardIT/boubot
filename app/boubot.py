import discord
from discord.utils import get
import aiohttp
import json
import glob, os
import random
from random import randrange
import time
import yaml
import requests


config_file = open(r'config.yaml')

#auth
config = yaml.load(config_file, Loader=yaml.FullLoader)
CLIENT_ID = config['AUTH']['CLIENT_ID']
CLIENT_SECRET = config['AUTH']['CLIENT_SECRET']
TOKEN = config['AUTH']['TOKEN']

EMOJI = config['EMOJI']
CHANNEL_ID = config['CHANNEL_ID']


MSG_HELP = "asdasdasd"

client = discord.Client()

__games__ = []
voice_channel = ""


def __get_gif__(key_word):
    rand_num = randrange(10)
    x = requests.get('https://api.tenor.com/v1/search?q='+key_word+'&limit='+str(rand_num))
    if x.status_code is 200:
        return x.json()['results'][rand_num-1]['url']
    else:
        return ''


def get_rand_theme():
    return random.choice(glob.glob("themes/*.json"))


def set_theme(theme_json):
    print(theme_json)


@client.event
async def on_message(message):

    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    #print(EMOJI['EGGPLANT'])
    await message.add_reaction(emoji='\U0001F44D')

    general_text = client.get_channel(CHANNEL_ID['GENERAL_TEXT'])
    general_vocal = client.get_channel(CHANNEL_ID['GENERAL_VOCAL'])


    if message.content.startswith('#gif'):
        key_word = message.content[5:]
        await general_text.send(__get_gif__(key_word))

    if message.content.startswith('#help'):
        await general_text.send(MSG_HELP)

    if message.content.startswith('#hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await general_text.send(msg)

    if message.content.startswith('#join'):
        voice_channel = await general_vocal.connect()

    if message.content.startswith('#leave'):
        for vc in client.voice_clients:
            if(vc.server == message.server):
                await vc.disconnect()

    if message.content.startswith('#newtheme'):
        await general_text.send(str(get_rand_theme()))

    if message.content.startswith('#add '):
        __games__.append(message.content[5:])
        await general_text.send("Done")

    if message.content.startswith('#list'):
        await general_text.send(str(__games__))

    if message.content.startswith('#roll'):
        await general_text.send(random.choice(__games__))

    if message.content.startswith('#clear'):
        __games__.clear()
        await general_text.send("Done")

    if message.content.startswith('#cat'):
        async with aiohttp.ClientSession() as session:
            async with session.get('http://aws.random.cat/meow') as r:
                if r.status == 200:
                    js = await r.json()
                    await general_text.send(js['file'])

    if message.content.startswith('#newpoll'):
        time.sleep(10)
        await general_text.send(str(message.reactions))


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(TOKEN)


