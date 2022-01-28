import os
import time

import discord
from dotenv import load_dotenv
import random

load_dotenv()

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


@client.event
async def on_voice_state_update(member, before, after):

    if member != client.user:
        if after.channel is not None and before.channel is None:
            if len(after.channel.members) == 1:  # if the user is not the bot and someone connects to the channel it plays a sound
                time.sleep(1)
                voiceclient = await after.channel.connect()  # wait x amount of seconds so it randomize joins
                speakrandom(voiceclient)



        if after.channel is not None:
            print(after.channel)

        if before.channel is not None:
            print(before.channel.members)
            if len(before.channel.members) == 1:
                for voice_state in client.voice_clients:
                    if voice_state.channel.id == before.channel.id:
                        await voice_state.disconnect()
                        print(voice_state.guild.id)
                        break



def speakrandom(voiceclient):
    time.sleep(2)  # wait 2 seconds so everybody is confest
    audio = audio_dir.get(random.randint(0, 9))  # get one of the audios (spezified in the audio dictionary)
    print(audio)
    voiceclient.play(discord.FFmpegPCMAudio(dir_path + fr'\\audio\\{audio}.mp3'))  # play sound


client.run(os.getenv("DISCORD_TOKEN"))
