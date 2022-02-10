import discord
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from vk_music.vk_audio.exc import *
from vk_music.vk_audio.VkAudio import VkAudio
from vk_api import VkApi
import config
from vk_music.Queues import Queues
from asyncio import get_event_loop


class VkMusic(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.voice_states = {}
        self.queues = Queues()

        vk = VkApi(config.vk_login, config.vk_password)
        vk.auth()
        self.vk_audio = VkAudio(vk)

    @commands.command(name='join')
    async def _join(self, ctx: commands.Context):
        channel: discord.VoiceChannel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            await channel.connect()

    @commands.command(name='play')
    async def play(self, ctx: commands.Context, *, song_name):
        await ctx.invoke(self._join)
        voice: discord.VoiceClient = get(self.bot.voice_clients, guild=ctx.guild)

        if self.queues.is_playing(voice):
            audio = await self.prepare_audio(ctx, voice, song_name, False)
            if audio:
                # loop = get_event_loop()
                print('add')
                self.queues.add(voice, lambda: voice.play(FFmpegPCMAudio(audio.path, executable='/usr/bin/ffmpeg'), after=lambda x: self.queues.get(voice)()))
            return

        self.queues.set_playing(voice, True)

        audio = await self.prepare_audio(ctx, voice, song_name)
        def debug(x):
            print('start new')
            self.queues.get(voice)()
        voice.play(FFmpegPCMAudio(audio.path, executable='/usr/bin/ffmpeg'), after=lambda x: debug)

    async def prepare_audio(self, ctx, voice, song_name, play_now=True):
        message = await ctx.send(':musical_note: Searching...')

        try:
            audio = self.vk_audio.download_song_by_name(song_name)
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

        if play_now:
            embed = audio.get_discord_embed('Now Playing', ctx.author)
        else:
            embed = audio.get_discord_embed(f'Add in Queue#{self.queues.size(voice) + 1}', ctx.author)
        await message.delete()
        await ctx.send(embed=embed)
        return audio

    self.play

    @commands.command()
    async def leave(self, ctx: commands.Context):
        voice: discord.VoiceClient = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.disconnect()

