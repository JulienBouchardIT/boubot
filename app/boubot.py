import discord
import aiohttp
import json
import glob, os
import random
import time
import yaml


#auth
with open(r'config.yaml') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)
    CLIENT_ID = config['CLIENT_ID']
    CLIENT_SECRET = config['CLIENT_SECRET']
    TOKEN = config['TOKEN']


#Channels ids
GENERAL_TEXT_ID = 420810552940429312
GENERAL_VOCAL_ID = 555198797001654285

MSG_HELP = "asdasdasd"

client = discord.Client()

__games__ = []
voice_channel = ""

def get_rand_theme():
    return random.choice(glob.glob("themes/*.json"))


def set_theme(theme_json):
    print(theme_json)


@client.event
async def on_message(message):

    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    general_text = client.get_channel(GENERAL_TEXT_ID)
    general_vocal = client.get_channel(GENERAL_VOCAL_ID)

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
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(TOKEN)


