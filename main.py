import os

import discord
from dotenv import load_dotenv

load_dotenv()

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected')

@client.event
async def on_voice_state_update(member, before, after):
    print(member)
    if after.channel != None:
        print(after.channel.id)
    print("###############")


client.run(os.getenv("DISCORD_TOKEN"))