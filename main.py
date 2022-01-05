import discord
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio

from VkAudio import VkAudio
from vk_api import VkApi

from requests import session

import config

from os import getcwd

TOKEN = config.token
client = commands.Bot(command_prefix='apb!')

session = session()
session.proxies = {'http': '85.26.146.169:80'}
vk = VkApi(config.vk_login, config.vk_password)
vk.auth()
vk_audio = VkAudio(vk)


@client.command()
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()


@client.command()
async def play(ctx, *song_name):
    audio = vk_audio.get_m3u8(' '.join(song_name))
    voice = get(client.voice_clients, guild=ctx.guild)
    voice.play(FFmpegPCMAudio(f'{getcwd()}/tmp/new.mp3', executable='/usr/bin/ffmpeg'))
    await ctx.send(f'Playing {audio}')
    await ctx.send(audio.img_url)


client.run(TOKEN)
