import requests
from random import choice


class Category:
    categories = ['waifu', 'neko', 'shinobu', 'megumin',
                  'bully', 'cuddle', 'cry', 'hug', 'awoo',
                  'kiss', 'lick', 'pat', 'smug', 'bonk',
                  'yeet', 'blush', 'smile', 'wave', 'highfive',
                  'handhold', 'nom', 'bite', 'glomp', 'slap',
                  'kill', 'kick', 'happy', 'wink', 'poke',
                  'dance', 'cringe']

    def __init__(self):
        for category in self.categories:
            setattr(self, category.upper(), category)


class WaifuApi:
    url = 'https://api.waifu.pics'

    def get_image(self, category):
        response = requests.get(f'{self.url}/sfw/{category}')
        if response.ok:
            image_url = response.json().get('url')
            return image_url
        return None

    def get_many_images(self, category, exclude_list=None):
        data = {'exclude': [""]}

        if exclude_list:
            data['exclude'] = exclude_list

        response = requests.post(f'{self.url}/many/sfw/{category}', data=data)
        if response.ok:
            image_urls = response.json().get('files')
            return image_urls
        return None

    def get_random_image(self):
        category = choice(Category.categories)
        return self.get_image(category)

    def get_random_many_images(self, exclude_list=None):
        category = choice(Category.categories)
        return self.get_many_images(category, exclude_list)
