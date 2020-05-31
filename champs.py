from selenium import webdriver
import os
import random
import json
import requests

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
                break

    def runes(self):
        #self.driver.set_window_size(689,1120) # May need manual adjustment        
        seed = str(random.randint(0,99999))
        self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div[5]/div[1]/div/div[1]/div/table/tbody[2]').screenshot('./temp/'+seed+'.png')
        return seed

    def build(self):
        seed = str(random.randint(0,99999))
        self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div[5]/div[1]/div/div[1]/table[2]').screenshot('./temp/'+seed+'.png')
        return seed

    def skills(self):
        seed = str(random.randint(0,99999))
        self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div[5]/div[1]/div/div[1]/table[1]/tbody[2]').screenshot('./temp/'+seed+'.png')
        return seed

    def champ_stats(self):
        #self.driver.set_window_size(1080,1920)
        seed = str(random.randint(0,99999))
        self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div[5]/div[1]/div/div[2]/div[1]').screenshot('./temp/'+seed+'.png')
        return seed
        
    def sums(self):
        seed = str(random.randint(0,99999))
        self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div[5]/div[1]/div/div[1]/table[1]/thead[1]').screenshot('./temp/'+seed+'.png')
        return seed

    def matchups(self):
        #S = lambda X: self.driver.execute_script('return document.querySelector("body > div > div.main-container > div.page-content > div.ng-scope > div.matchups > div > div.row.counter-row").scroll'+X)
        #self.driver.set_window_size(S('Width')+200,S('Height')+200)
        seed = str(random.randint(0,99999))
        self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div[5]/div[7]/div/div[2]/div[3]').screenshot('./temp/'+seed+'.png')
        return seed
