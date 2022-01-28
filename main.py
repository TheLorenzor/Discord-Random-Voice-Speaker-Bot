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
    if member != client.user:  # to ignore actions by the bot
        if after.channel is not None and before.channel is None:  # if someone is joining

            isInGuildConencted = False
            voice = None

            for voiceClient in client.voice_clients:
                if voiceClient.channel.guild.id == after.channel.guild.id:
                    voice = voiceClient
                    isInGuildConencted = True

            if isInGuildConencted:  # if it is already connected
                if voice.channel.id == after.channel.id:  # if he connects to one where one is already in it
                    time.sleep(5)
                    speakrandom(voice)
                else:
                    time.sleep(1)
                    permissions = after.channel.permissions_for(
                        client.get_guild(after.channel.guild.id).get_member(client.user.id))
                    if permissions.speak and permissions.connect:
                        voiceClient = await after.channel.connect()
                        speakrandom(voiceClient)
                    else:
                        print(f"cant connect to {after.channel}")

            else:  # if it is new there it connects to it
                time.sleep(1)
                permissions = after.channel.permissions_for(
                    client.get_guild(after.channel.guild.id).get_member(client.user.id))
                if permissions.speak and permissions.connect:
                    voiceClient = await after.channel.connect()
                    speakrandom(voiceClient)
                else:
                    print(f"cant connect to {after.channel}")

        if before.channel is not None and after.channel is None:  # if someone is leaving
            if len(before.channel.members) == 1:
                for voice_state in client.voice_clients:
                    if voice_state.channel.id == before.channel.id:
                        await voice_state.disconnect()
                        break

        if before.channel is not None and after.channel is not None:
            print(before)

def speakrandom(voiceclient):
    time.sleep(2)  # wait 2 seconds so everybody is confest
    audio = audio_dir.get(random.randint(0, 9))  # get one of the audios (spezified in the audio dictionary)
    print(audio)
    voiceclient.play(discord.FFmpegPCMAudio(dir_path + fr'\audio\{audio}.mp3'))  # play sound


def randomvoiceSpeak():
    while (True):
        if len(client.voice_clients) == 0:
            break
        else:
            time.sleep(random.randint(0, 60))  # maximal eine stunde wo nichts passiert
            for voice_client in client.voice_clients:
                speakrandom(voice_client)


client.run(os.getenv("DISCORD_TOKEN"))
