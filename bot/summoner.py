import random
import os
import json
import requests
from dotenv import load_dotenv
from riotwatcher import LolWatcher

load_dotenv()

class Summon():
    def __init__(self, name, region="na1", prefix="na"):
        lol_watcher = LolWatcher(os.getenv("RIOT_API_KEY"))
        try:
            player_info = lol_watcher.summoner.by_name(region, name)
            player_stats = lol_watcher.league.by_summoner(region, player_info['id'])
            self.real_player = True
        except Exception as e:
            print(e)
            print('bad input for summoner or region')
            self.real_player = False
        if self.real_player:
            self.name = player_info['name']
            self.icon = player_info['profileIconId']
            self.level = player_info['summonerLevel']
            response = requests.get('https://ddragon.leagueoflegends.com/cdn/10.10.3216176/data/en_US/champion.json').json()['data']
            try:
                if len(player_stats) >= 2:
                    for i in player_stats:
                        if i["queueType"] == "RANKED_SOLO_5x5":
                            self.ranksolo = f'{i["tier"].lower().capitalize()} {i["rank"]} {i["leaguePoints"]} LP'
                        elif i["queueType"] == "RANKED_FLEX_SR":
                            self.rank5 = f'{i["tier"].lower().capitalize()} {i["rank"]} {i["leaguePoints"]} LP' 
                else:
                    self.ranksolo = f'{player_stats[0]["tier"].lower().capitalize()} {player_stats[0]["rank"]} {player_stats[0]["leaguePoints"]} LP'
                    self.rank5 = None
            except IndexError:
                self.ranksolo ='Unranked'
                self.rank5 = 'Unranked'
            if self.ranksolo != 'Unranked':
                self.win = f'{round((player_stats[0]["wins"] / (player_stats[0]["wins"] + player_stats[0]["losses"])) * 100)}%'
            else:
                self.win = 'N/A' 
            try:
                mastery = requests.get(f'https://{region}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{player_info["id"]}?api_key={os.getenv("RIOT_API_KEY")}').json()
                for champ in response:
                    if response[champ]['key'] == str(mastery[0]['championId']):
                        self.champ = f"{response[champ]['name']} {mastery[0]['championPoints']}"
                        self.img = f"https://ddragon.leagueoflegends.com/cdn/10.10.3216176/img/champion/{response[champ]['image']['full']}"
                        break
            except:
                self.champ = "n/a"
                self.champ = "./images/default.png"
                print('masteries were not found')
            self.url = f'https://{prefix}.op.gg/summoner/username={name}'
