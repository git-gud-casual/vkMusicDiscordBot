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
        if channel:
            if voice and voice.is_connected() and voice.channel != channel.id:
                self.queues.remove(voice)
                await voice.move_to(channel)
            else:
                await channel.connect()
        else:
            embed = discord.Embed(title='Error', color=discord.Color.red())
            embed.description = 'You are not in voice channel'
            await ctx.send(embed=embed)

    @commands.command(name='play')
    async def play(self, ctx: commands.Context, *, song_name):
        voice: discord.VoiceClient = get(self.bot.voice_clients, guild=ctx.guild)
        if not voice:
            await ctx.invoke(self._join)
            voice: discord.VoiceClient = get(self.bot.voice_clients, guild=ctx.guild)

        if self.queues.is_playing(voice):
            queue = self.queues.add_size(voice)
            audio = await self.prepare_audio(ctx, song_name, False, queue)
            if audio:
                loop = get_event_loop()
                self.queues.add(voice, lambda: voice.play(FFmpegPCMAudio(audio.path, executable='/usr/bin/ffmpeg'),
                                                          after=self.get_after_func(voice, loop)))
            return

        self.queues.set_playing(voice, True)

        audio = await self.prepare_audio(ctx, song_name)
        voice.play(FFmpegPCMAudio(audio.path, executable='/usr/bin/ffmpeg'), after=self.get_after_func(voice))

    def get_after_func(self, voice, loop):
        return lambda x: loop.run_until_complete(voice.disconnect()) if self.queues.get(voice)() == 0 else 0

    async def prepare_audio(self, ctx, song_name, play_now=True, queue_num=None):
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
            embed = audio.get_discord_embed(f'Add in Queue#{queue_num}', ctx.author)
        await message.delete()
        await ctx.send(embed=embed)
        return audio

    @commands.command()
    async def stop(self, ctx: commands.Context):
        voice: discord.VoiceClient = get(self.bot.voice_clients, guild=ctx.guild)
        self.queues.remove(voice)
        if voice and voice.is_connected():
            await voice.disconnect()
