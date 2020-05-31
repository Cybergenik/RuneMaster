from selenium import webdriver
import random
import os
import json
import requests
from riotwatcher import LolWatcher

RIOT_API_KEY = os.getenv("RIOT_API_KEY")
lol_watcher = LolWatcher(RIOT_API_KEY)

class Summon():
    def __init__(self, region="na1", name="jareco", driver=None):
        try:
            player_info = lol_watcher.summoner.by_name(region, name)
            player_stats = lol_watcher.league.by_summoner(region, player_info['id'])
            self.real_player = True
        except:
            print('bad input for summoner or region')
            self.real_player = False
        if self.real_player:
            self.name = player_info['name']
            self.icon = player_info['profileIconId']
            self.level = player_info['summonerLevel']
            response = requests.get('https://ddragon.leagueoflegends.com/cdn/10.10.3216176/data/en_US/champion.json').json()['data']
            try:
                self.rank = f'{player_stats[0]["tier"].lower().capitalize()} {player_stats[0]["rank"]} {player_stats[0]["leaguePoints"]} LP'
            except IndexError:
                self.rank ='Unranked'
            if self.rank != 'Unranked':
                self.win = f'{round((player_stats[0]["wins"] / (player_stats[0]["wins"] + player_stats[0]["losses"])) * 100)}%'
            else:
                self.win = 'N/A' 
            with open('regions.json') as f:
                regions = json.load(f)
            for reg in regions:
                if regions[reg] == region:
                    try:
                        mastery = requests.get(f'https://{regions[reg]}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{player_info["id"]}?api_key={RIOT_API_KEY}').json()
                        for champ in response:
                            if response[champ]['key'] == str(mastery[0]['championId']):
                                self.champ = f"{response[champ]['name']} {mastery[0]['championPoints']}"
                                self.img = f"https://ddragon.leagueoflegends.com/cdn/10.10.3216176/img/champion/{response[champ]['image']['full']}"
                                break
                        self.masteries = True
                    except:
                        self.masteries = False
                    self.url = 'https://'+reg+'.op.gg/summoner/userName='+name
                    break
            if driver != None:
               self.driver = driver
               self.driver.get(self.url)

    def get_match_info(self):
        seed = str(random.randint(0,99999))
        self.driver.find_element_by_xpath('//*[@id="GameAverageStatsBox-summary"]/div[1]').screenshot('./temp/'+seed+'.png')
        return seed

    def get_matches(self):
        seed = str(random.randint(0,99999))
        self.driver.set_window_size(1080,1920) # May need manual adjustment
        self.driver.find_element_by_xpath('//*[@id="SummonerLayoutContent"]/div[2]/div[2]/div').screenshot('./temp/'+seed+'.png')
        return seed
