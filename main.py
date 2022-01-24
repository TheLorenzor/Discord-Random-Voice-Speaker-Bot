import os
import time

import discord
from dotenv import load_dotenv
from playsound import playsound
import random
load_dotenv()

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected')

@client.event
async def on_voice_state_update(member, before, after):
    print(member)
    if after.channel != None and member!=client.user:
        time.sleep(1)
        await after.channel.connect()
        time.sleep(2)


    print("###############")


client.run(os.getenv("DISCORD_TOKEN"))