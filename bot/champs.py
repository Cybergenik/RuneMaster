from selenium import webdriver
import os
import random
import json
import requests
from time import sleep

class Champ():
    def __init__(self, champs, version, champ):
        self.champ = champs[champ]['id']
        self.title = champs[self.champ]['title']
        self.img = f"https://ddragon.leagueoflegends.com/cdn/{version}/img/champion/{champs[self.champ]['image']['full']}"
        self.desc =  champs[self.champ]['blurb']
        self.tags = ' '.join(champs[self.champ]['tags'])
        self.stats = f'Health: {champs[self.champ]["stats"]["hp"]} \n \
                    Move Speed: {champs[self.champ]["stats"]["movespeed"]} \n \
                    Attack Damage: {champs[self.champ]["stats"]["attackdamage"]} \n \
                    Attack Range: {champs[self.champ]["stats"]["attackrange"]} \n \
                    Attack Speed: {champs[self.champ]["stats"]["attackspeed"]}'
        self.url = f'https://www.op.gg/champion/{self.champ}/statistics'
        self.real = True 
        self.name = champs[champ]['name']
                
