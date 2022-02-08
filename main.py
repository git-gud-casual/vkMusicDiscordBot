from discord.ext import commands
import config
from vk_music.VkMusic import VkMusic
from anime.Anime import Anime


TOKEN = config.token
client = commands.Bot(command_prefix='phonk!')

if __name__ == "__main__":
    client.add_cog(VkMusic(client))
    client.add_cog(Anime(client))
    client.run(TOKEN)
