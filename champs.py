import json
import requests

class Champ:
    def __init__(self, champ):
        response = requests.get('https://ddragon.leagueoflegends.com/cdn/10.10.3216176/data/en_US/champion.json')

        self.real = False
        for name in response.json()['data']:
            if champ == name.lower():
                self.champ = response.json()['data'][name]['name']
                self.title = response.json()['data'][self.champ]['title']
                self.img = 'https://ddragon.leagueoflegends.com/cdn/10.10.3216176/img/champion/'+response.json()['data'][self.champ]['image']['full']
                self.desc =  response.json()['data'][self.champ]['blurb']
                self.tags = ''
                for _ in response.json()['data'][self.champ]['tags']:
                    self.tags = _+" "+self.tags
                self.stats = f'Health: {response.json()["data"][self.champ]["stats"]["hp"]} \n \
                            Move Speed: {response.json()["data"][self.champ]["stats"]["movespeed"]} \n \
                            Attack Damage: {response.json()["data"][self.champ]["stats"]["attackdamage"]} \n \
                            Attack Range: {response.json()["data"][self.champ]["stats"]["attackrange"]} \n \
                            Attack Speed: {response.json()["data"][self.champ]["stats"]["attackspeed"]}'
                self.real = True 
                break

    def get_real(self):
        return self.real
    def get_champ(self):
        return self.champ
    def get_title(self):
        return self.title
    def get_img(self):
        return self.img
    def get_desc(self):
        return self.desc
    def get_tags(self):
        return self.tags
    def get_stats(self):
        return self.stats
                
