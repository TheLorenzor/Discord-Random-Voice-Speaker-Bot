import os
import time
import random
import threading
import logging
import discord

import constants as const

client = discord.Client(intents=discord.Intents.default())
dir_path = os.getcwd()
logging.basicConfig(level=logging.INFO)

audio_files_path =const.DATA_PATH / 'audio'
audio_files = list(audio_files_path.glob('*.mp3'))
@client.event
async def on_ready():
    print(f"{client.user} is Ready") 
    if const.IS_UPDATE: # check whether at all it should be send
        for guild in client.guilds:
            for channel in guild.text_channels: 
                user_member = guild.get_member(client.user.id)
                permission =channel.permissions_for(user_member)
                if permission.view_channel and permission.send_messages:                
                    await channel.send(const.UPDATE_MESSAGE)
                    break


@client.event
async def on_voice_state_update(member, before, after):
    if member != client.user:  # to ignore actions by the bot
        if after.channel is not None and before.channel is None:  # if someone is joining
            isInGuildConencted = False
            voice = None
            for voiceClient in client.voice_clients:  # checks if the bot is already connected to the guild
                if voiceClient.channel.guild.id == after.channel.guild.id:
                    voice = voiceClient
                    isInGuildConencted = True
                    break

            if isInGuildConencted:  # if it is already connected
                if voice.channel.id != after.channel.id:  # if he connects to one where he is not in it
                    time.sleep(1)
                    permissions = after.channel.permissions_for(
                        client.get_guild(after.channel.guild.id).get_member(client.user.id))
                    if permissions.speak and permissions.connect:  # checks whether the bot has the priviliges to speak and connect to the voice channel
                        voice.move_to(after.channel)

            else:  # if it is new there it connects to it
                time.sleep(1)
                permissions = after.channel.permissions_for(
                    client.get_guild(after.channel.guild.id).get_member(client.user.id))

                if permissions.speak and permissions.connect:  # checks whether the bot has the priviliges to speak and connect to the voice channel
                    await after.channel.connect()
                    # connects to Voice channel then checks whether it is the first random
                    if not any(threads.name == "RandomSpeak" for threads in threading.enumerate()):
                        voiceSpeakThread = threading.Thread(target=randomvoiceSpeak)
                        voiceSpeakThread.start()
                        voiceSpeakThread.name = "RandomSpeak"
        if before.channel is not None and after.channel is None:  # if someone is leaving
            voice_state = None

            for voice_state in client.voice_clients:
                if voice_state.channel.id == before.channel.id:
                    voice_state = voice_state
                    break
            # if the voice state is part of the guild and if the mbot is the last one left
            if voice_state != None and len(voice_state.channel.members) == 1:
                await voice_state.disconnect()
                voiceChannels = voice_state.guild.voice_channels
                for voicechannel in voiceChannels:  # checks every voice channel
                    # if there is someone inside
                    if len(voicechannel.members) > 0 and any(member.name != client.user.name for member in
                                                             voicechannel.members):
                        # get the permission for the specific voice channel
                        permissions = voicechannel.permissions_for(client.get_guild(voicechannel.guild.id).get_member(
                                client.user.id))
                        # if he can speak and connect he connects else he doesnt move
                        if permissions.speak and permissions.connect:
                            await voicechannel.connect()

        if before.channel is not None and after.channel is not None:  # if someone is switching
            permissions = after.channel.permissions_for(
                client.get_guild(after.channel.guild.id).get_member(client.user.id))
            # if the channel memvvers where the person is now has more members than the current one
            if (len(after.channel.members) >= len(before.channel.members)) and permissions.speak and permissions.connect:
                # he switches to annoy the most people possible -> then moves to the location
                for voice_state in client.voice_clients:
                    if voice_state.channel.guild.id == before.channel.guild.id:
                        await voice_state.move_to(after.channel)
                        break


def speakrandom(voiceclient):
    audio = audio_files[random.randint(0,len(audio_files)-1)]  # get one of the audios (spezified in the audio dictionary)
    if voiceclient.is_connected():
        voiceclient.play(discord.FFmpegPCMAudio(str(const.DATA_PATH /'audio'/ audio)))  # play sound

@client.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        user_member = guild.get_member(client.user.id)
        permission = channel.permissions_for(user_member)
        if permission.view_channel and permission.send_messages:
            await channel.send(const.JOIN_MESSAGE)
            break

def randomvoiceSpeak():
    logging.info("starting with the speaker")
    while (True):
        if len(client.voice_clients) == 0:  # if there no voice clients anymore
            break
        for voice_client in client.voice_clients:
            speakrandom(voice_client)
        time.sleep(random.randint(5, const.TIMEOUT_TIME))  # maximal eine stunde wo nichts passiert


client.run(const.DISCORD_TOKEN)
