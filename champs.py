from selenium import webdriver
import os
import random
import json
import requests
from time import sleep

class Champ():
    def __init__(self, champ, driver=None):
        response = requests.get('https://ddragon.leagueoflegends.com/cdn/10.10.3216176/data/en_US/champion.json').json()['data']
        self.real = False
        for name in response:
            if champ == name.lower():
                self.champ = response[name]['id']
                self.title = response[self.champ]['title']
                self.img = f"https://ddragon.leagueoflegends.com/cdn/10.10.3216176/img/champion/{response[self.champ]['image']['full']}"
                self.desc =  response[self.champ]['blurb']
                self.tags = ' '.join(response[self.champ]['tags'])
                self.stats = f'Health: {response[self.champ]["stats"]["hp"]} \n \
                            Move Speed: {response[self.champ]["stats"]["movespeed"]} \n \
                            Attack Damage: {response[self.champ]["stats"]["attackdamage"]} \n \
                            Attack Range: {response[self.champ]["stats"]["attackrange"]} \n \
                            Attack Speed: {response[self.champ]["stats"]["attackspeed"]}'
                self.url = f'https://www.op.gg/champion/{self.champ}/statistics'
                self.real = True 
                self.name = response[name]['name']
                
