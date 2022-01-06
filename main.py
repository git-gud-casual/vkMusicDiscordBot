import discord
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio

from vk_audio.VkAudio import VkAudio
from vk_audio.exc import *

from vk_api import VkApi

import config


TOKEN = config.token
client = commands.Bot(command_prefix='phonk!')

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
        else:
            await channel.connect()

    @commands.command()
    async def play(self, ctx: commands.Context, *song_name):

        message = await ctx.send(':musical_note: Searching...')

        voice: discord.VoiceClient = get(client.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            await message.delete()
            await ctx.send('Bot is playing now')
            return

        song_name = ' '.join(song_name)

        try:
            audio = vk_audio.download_song_by_name(song_name)
        except Exception as e:
            embed = discord.Embed(title='Error', color=discord.Color.red())

            if isinstance(e, AudioNotFoundException):
                msg = 'Song not found'
            elif isinstance(e, AssertionError):
                msg = 'Bad request'
            elif isinstance(e, AudioNotAvailable):
                msg = 'Audio not available'
            else:
                msg = 'Unknown error'
                print(e)

            embed.description = msg
            await message.delete()
            await ctx.send(embed=embed)
            return

        await ctx.invoke(self._join)

        embed = audio.get_discord_embed('Now Playing', ctx.author)
        await message.delete()
        await ctx.send(embed=embed)

        voice: discord.VoiceClient = get(client.voice_clients, guild=ctx.guild)
        voice.play(FFmpegPCMAudio(audio.dir + '/index.m3u8', executable='/usr/bin/ffmpeg'))

    @commands.command()
    async def leave(self, ctx: commands.Context):
        voice: discord.VoiceClient = get(client.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.disconnect()


client.add_cog(Music(client))
client.run(TOKEN)
