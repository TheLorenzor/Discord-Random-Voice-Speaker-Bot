import os
import time

import discord
from dotenv import load_dotenv
import random

load_dotenv()

random.seed(12749012743)
client = discord.Client()
dir_path = os.getcwd()

audio_dir = {
    0: 'akkurat',
    1: 'cringe',
    2: 'digga',
    3: 'geringverdiener',
    4: 'mittwoch',
    5: 'pappatastisch',
    6: 'same',
    7: 'sheesh',
    8: 'sus',
    9: 'wild'
}


@client.event
async def on_ready():
    print(f'{client.user} has connected')
    print(client.guilds)


@client.event
async def on_voice_state_update(member, before, after):
    print(member)
    if after.channel != None and member != client.user:
        time.sleep(1)
        voiceClient = await after.channel.connect()
        time.sleep(2)
        audio = audio_dir.get(random.randint(0, 9))
        print(audio)
        voiceClient.play(discord.FFmpegPCMAudio(dir_path + fr'\\audio\\{audio}.mp3'))



client.run(os.getenv("DISCORD_TOKEN"))
