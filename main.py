import os
import time
import discord
from dotenv import load_dotenv
import random
import threading
import log

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
    log.log(0,"Bot ist gestartet")

@client.event
async def on_voice_state_update(member, before, after):
    if member != client.user:  # to ignore actions by the bot
        if after.channel is not None and before.channel is None:  # if someone is joining
            try:
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
                            log.log(1,"Can't Connect to "+after.channel)

                else:  # if it is new there it connects to it
                    time.sleep(1)
                    permissions = after.channel.permissions_for(
                        client.get_guild(after.channel.guild.id).get_member(client.user.id))

                    if permissions.speak and permissions.connect: #checks whether the bot has the priviliges to speak and connect to the voice channel
                        voiceClient = await after.channel.connect()
                        log.log(0,f"Connected to {after.channel} / Guild --> {voiceClient.guild}")

                        #connects to Voice channel then checks whether it is the first random 
                        if not any(threads.name=="RandomSpeak" for threads in threading.enumerate()): 
                            log.log(0,"Started Thread")
                            voiceSpeakThread = threading.Thread(target=randomvoiceSpeak)
                            voiceSpeakThread.start()
                            voiceSpeakThread.name = "RandomSpeak"
                    else:
                        log.log(1,"Can't Connect to "+after.channel)
            except:
                log.log(2,"Error with joining Discord")

        if before.channel is not None and after.channel is None:  # if someone is leaving
            try:
                voice_state = None

                for voice_state in client.voice_clients:
                    if voice_state.channel.id == before.channel.id:
                        voice_state = voice_state
                        break

                if voice_state!= None and len(voice_state.channel.members) ==1: #if the voice state is part of the guild and if the mbot is the last one left
                    await voice_state.disconnect()
                    log.log(0,f"Joined {voice_state.channel} / Guild --> {voice_state.guild}")

                    voiceChannels = voice_state.guild.voice_channels
                    for voicechannel in voiceChannels: #checks every voice channel
                        if len(voicechannel.members) >0 and any(member.name != client.user.name for member in voicechannel.members) : #if there is someone inside
                            permissions = voicechannel.permissions_for(
                                client.get_guild(voicechannel.guild.id).get_member(client.user.id)) #get the permission for the specific voice channel
                            if permissions.speak and permissions.connect: #if he can speak and connect he connects else he doesnt move
                                await voicechannel.connect()
                                break
            except:
                log.log(2,"Error while someone leaving the channel")

        if before.channel is not None and after.channel is not None: #if someone is switching
            try:
                permissions = after.channel.permissions_for(
                                    client.get_guild(after.channel.guild.id).get_member(client.user.id))
                if (len(after.channel.members) >= len(before.channel.members)) and permissions.speak and permissions.connect: #if the channel memvvers where the person is now has more members than the current one
                    # he switches to annoy the most people possible -> then moves to the location
                    for voice_state in client.voice_clients:
                        if voice_state.channel.guild.id == before.channel.guild.id:
                            await voice_state.move_to(after.channel)
                            log.log(0,f"Moving from Channel: {before.channel} -> {after.channel} | Guild -> {voice_state.guild}")
                            break
            except:
                log.log(2,"Error while switching channel")


def speakrandom(voiceclient):
    time.sleep(2)  # wait 2 seconds so everybody is confest
    audio = audio_dir.get(random.randint(0, 9))  # get one of the audios (spezified in the audio dictionary)
    try:
        if voiceclient.is_connected():
            voiceclient.play(discord.FFmpegPCMAudio(f'.\\audio\\{audio}.mp3'))  # play sound
            log.log(0,f"playing {audio} /Guild -> {voiceclient.guild} /Channel -> {voiceclient.channel}")
    except:
        log.log(2,"Error with playing the audio")

def randomvoiceSpeak():
    try:
        while (True):
            if len(client.voice_clients) == 0: #if there no voice clients anymore
                log.log(0,"Closing Thread")
                break
            else:
                for voice_client in client.voice_clients:
                    speakrandom(voice_client)
                time.sleep(random.randint(0, int(os.getenv("MAX_TIME"))))  # maximal eine stunde wo nichts passiert
    except:
        log.log(2,"Error in Thread")


client.run(os.getenv("DISCORD_TOKEN"))
