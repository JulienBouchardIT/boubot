import discord
from discord.utils import get
import aiohttp
import glob
import random
from random import randrange
import time
import requests
import os

#auth
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
TOKEN = os.environ['TOKEN']

CHANNEL_ID = os.environ['CHANNEL_ID']



MSG_HELP = "asdasdasd"

client = discord.Client()

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


def get_rand_theme():
    return random.choice(glob.glob("themes/*.json"))


def set_theme(theme_json):
    print(theme_json)


@client.event
async def on_message(message):

    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('test'):
        author = message.author
        await message.channel.send('I heard you! {0.name}'.format(author))

    # await message.add_reaction(emoji='\U0001F44D')

    general_text = client.get_channel(CHANNEL_ID)
    # general_vocal = client.get_channel(CHANNEL_ID)


    if message.content.startswith('#gif'):
        key_word = message.content[5:]
        await general_text.send(__get_gif__(key_word))

    if message.content.startswith('#help'):
        await general_text.send(MSG_HELP)

    if message.content.startswith('#hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await general_text.send(msg)

    # if message.content.startswith('#join'):
    #    voice_channel = await general_vocal.connect()

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
