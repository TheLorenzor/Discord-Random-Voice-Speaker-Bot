import os
import time

import discord
from dotenv import load_dotenv
import random
import threading
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

            for voiceClient in client.voice_clients: #checks if the bot is already connected to the guild
                if voiceClient.channel.guild.id == after.channel.guild.id:
                    voice = voiceClient
                    isInGuildConencted = True

            if isInGuildConencted:  # if it is already connected
                if voice.channel.id != after.channel.id:  # if he connects to one where he is not in it
                    time.sleep(1)
                    permissions = after.channel.permissions_for(
                        client.get_guild(after.channel.guild.id).get_member(client.user.id))
                    if permissions.speak and permissions.connect: #checks whether the bot has the priviliges to speak and connect to the voice channel
                        voice.move_to(after.channel)
                    else:
                        print(f"cant connect to {after.channel}")

            else:  # if it is new there it connects to it
                time.sleep(1)
                permissions = after.channel.permissions_for(
                    client.get_guild(after.channel.guild.id).get_member(client.user.id))
                if permissions.speak and permissions.connect: #checks whether the bot has the priviliges to speak and connect to the voice channel
                    voiceClient = await after.channel.connect()
                    #connects to Voice channel then checks whether it is the first random 
                    if not any(threads.name=="RandomSpeak" for threads in threading.enumerate()): 
                        voiceSpeakThread = threading.Thread(target=randomvoiceSpeak)
                        voiceSpeakThread.start()
                        voiceSpeakThread.name = "RandomSpeak"
                    print(threading.enumerate())
                else:
                    print(f"cant connect to {after.channel}")

        if before.channel is not None and after.channel is None:  # if someone is leaving
            voice_state = None

            for voice_state in client.voice_clients:
                if voice_state.channel.id == before.channel.id:
                    voice_state = voice_state
                    break

            if voice_state!= None and len(voice_state.channel.members) ==1: #if the voice state is part of the guild and if the mbot is the last one left
                await voice_state.disconnect()
                voiceChannels = voice_state.guild.voice_channels
                for voicechannel in voiceChannels: #checks every voice channel
                    if len(voicechannel.members) >0 and any(member.name != client.user.name for member in voicechannel.members) : #if there is someone inside
                        permissions = voicechannel.permissions_for(
                            client.get_guild(voicechannel.guild.id).get_member(client.user.id)) #get the permission for the specific voice channel
                        if permissions.speak and permissions.connect: #if he can speak and connect he connects else he doesnt move
                            await voicechannel.connect()
                            break

        if before.channel is not None and after.channel is not None: #if someone is switching
            permissions = after.channel.permissions_for(
                                client.get_guild(after.channel.guild.id).get_member(client.user.id))
            if (len(after.channel.members) >= len(before.channel.members)) and permissions.speak and permissions.connect: #if the channel memvvers where the person is now has more members than the current one
                # he switches to annoy the most people possible -> then moves to the location
                for voice_state in client.voice_clients:
                    if voice_state.channel.guild.id == before.channel.guild.id:
                       await voice_state.move_to(after.channel)
                       break


def speakrandom(voiceclient):
    time.sleep(2)  # wait 2 seconds so everybody is confest
    audio = audio_dir.get(random.randint(0, 9))  # get one of the audios (spezified in the audio dictionary)
    if voiceclient.is_connected():
        print(audio)
        voiceclient.play(discord.FFmpegPCMAudio(dir_path + fr'\audio\{audio}.mp3'))  # play sound

def randomvoiceSpeak():
    while (True):
        if len(client.voice_clients) == 0: #if there no voice clients anymore
            break
        else:
            for voice_client in client.voice_clients:
                speakrandom(voice_client)
            time.sleep(random.randint(0, 10))  # maximal eine stunde wo nichts passiert


client.run(os.getenv("DISCORD_TOKEN"))
