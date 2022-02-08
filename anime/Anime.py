from discord.ext import commands
from anime.waifu_pics_api.WaifuApi import WaifuApi


class Anime(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.waifu_api = WaifuApi()

    @commands.command()
    async def anime(self, ctx: commands.Context):
        image_url = self.waifu_api.get_random_image()
        if image_url:
            await ctx.send(image_url)
        else:
            await ctx.send('Error')

    @commands.command()
    async def anime_ddos(self, ctx: commands.Context):
        image_urls = self.waifu_api.get_random_many_images()
        if image_urls:
            for url in image_urls:
                await ctx.send(url)
        else:
            await ctx.send('Error')
