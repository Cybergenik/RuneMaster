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
                if driver != None:
                    self.driver = driver
                    self.driver.get(self.url)
                    self.driver.execute_script('document.querySelector("#beacon-container").remove()')
                break

    def runes(self):
        self.driver.set_window_size(733,481)
        seed = str(random.randint(0,99999))
        self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div[5]/div[1]/div/div[1]/div/table/tbody[2]').screenshot(f'./temp/{seed}.png')
        return seed

    def build(self):
        self.driver.set_window_size(733,680)
        seed = str(random.randint(0,99999))
        self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div[5]/div[1]/div/div[1]/table[2]').screenshot(f'./temp/{seed}.png')
        return seed

    def skills(self):
        self.driver.set_window_size(734,150)
        seed = str(random.randint(0,99999))
        self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div[5]/div[1]/div/div[1]/table[1]/tbody[2]').screenshot(f'./temp/{seed}.png')
        return seed

    def champ_stats(self):
        self.driver.set_window_size(334,692)
        seed = str(random.randint(0,99999))
        self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div[5]/div[1]/div/div[2]/div[1]/div[2]').screenshot(f'./temp/{seed}.png')
        return seed
        
    def sums(self):
        self.driver.set_window_size(750,135)
        seed = str(random.randint(0,99999))
        self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div[5]/div[1]/div/div[1]/table[1]/tbody[1]').screenshot(f'./temp/{seed}.png')
        return seed

    def matchups(self):
        self.driver.set_window_size(342,620)
        self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div[1]/div/ul/li[6]/a').click()
        seed = str(random.randint(0,99999))
        sleep(1)
        self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div[5]/div[7]/div/div[2]/div[3]').screenshot(f'./temp/{seed}.png')
        return seed
