import discord
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio

from vk_audio.VkAudio import VkAudio
from vk_api import VkApi

from requests import session

import config

from vk_audio.exc import *

TOKEN = config.token
client = commands.Bot(command_prefix='phonk!')

session = session()
session.proxies = {'http': '85.26.146.169:80',
                   'https': '176.120.193.111:55443'}
vk = VkApi(config.vk_login, config.vk_password)
vk.auth()
vk_audio = VkAudio(vk)


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.voice_states = {}

    @commands.command(name='join', invoke_without_subcommand=True)
    async def _join(self, ctx: commands.Context):
        channel: discord.VoiceChannel = ctx.message.author.voice.channel
        voice = get(client.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        await channel.connect()

    @commands.command()
    async def play(self, ctx: commands.Context, *song_name):
        await ctx.invoke(self._join)

        song_name = ' '.join(song_name)

        try:
            audio = vk_audio.download_song_by_name(song_name)
        except Exception as e:
            if isinstance(e, AudioNotFoundException):
                await ctx.send('Song not found')
            elif isinstance(e, AssertionError):
                await ctx.send('Bad request')
            else:
                await ctx.send('Unknown error')
                raise e
            return

        voice = get(client.voice_clients, guild=ctx.guild)
        voice.play(FFmpegPCMAudio(f'tmp/new.mp3', executable='/usr/bin/ffmpeg'))

        await ctx.send(f'Playing {audio}')
        await ctx.send(audio.img_url)


client.add_cog(Music(client))
client.run(TOKEN)
