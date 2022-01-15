from dataclasses import dataclass
import requests
from riotwatcher import LolWatcher
from bot.utils import RIOT_API_KEY, get_version, get_champs

@dataclass
class Player():
    """Model for representing League of Legends player"""
    name: str
    url: str
    level: str
    icon_img: str
    ranksolo: str
    rank5: str
    win: str
    champ: str
    img: str

class Players():
    """Singleton class to dynamically generates player data"""
    def __init__(self):
        self.riot = LolWatcher(RIOT_API_KEY)
    
    def get_player(self, name, region="na1", prefix="na") -> Player:
        if prefix == "kr": prefix = "www"
        try:
            player_info = self.riot.summoner.by_name(region, name)
            player_stats = self.riot.league.by_summoner(region, player_info['id'])
        except Exception as e:
            print(f'Unable to load plater data from Riot API: \n {e}')
            return None
        else:
            _name = player_info['name']
            url = f'https://{prefix}.op.gg/summoner/userName={name}'
            level = player_info['summonerLevel']
            icon_img = f"https://ddragon.leagueoflegends.com/cdn/{get_version()}/img/profileicon/{player_info['profileIconId']}.png"
            try:
                if len(player_stats) >= 2:
                    for i in player_stats:
                        if i["queueType"] == "RANKED_SOLO_5x5":
                            ranksolo = f'{i["tier"].lower().capitalize()} {i["rank"]} {i["leaguePoints"]} LP'
                        elif i["queueType"] == "RANKED_FLEX_SR":
                            rank5 = f'{i["tier"].lower().capitalize()} {i["rank"]} {i["leaguePoints"]} LP' 
                else:
                    ranksolo = f'{player_stats[0]["tier"].lower().capitalize()} {player_stats[0]["rank"]} {player_stats[0]["leaguePoints"]} LP'
                    rank5 = None
            except IndexError:
                ranksolo = 'Unranked'
                rank5 = 'Unranked'
            if ranksolo != 'Unranked':
                win = f'{round((player_stats[0]["wins"] / (player_stats[0]["wins"] + player_stats[0]["losses"])) * 100)}%'
            else:
                win = 'N/A' 
            try:
                mastery = requests.get(f'https://{region}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{player_info["id"]}?api_key={RIOT_API_KEY}').json()
                for champ in get_champs():
                    if get_champs()[champ]['key'] == str(mastery[0]['championId']):
                        _champ = f"{get_champs()[champ]['name']} {mastery[0]['championPoints']}"
                        img = f"https://ddragon.leagueoflegends.com/cdn/{get_version()}/img/champion/{get_champs()[champ]['image']['full']}"
                        break
            except:
                champ = "N/A"
                img = "N/A"
                
            return Player(
                name=_name,
                url=url,
                level=level,
                icon_img=icon_img,
                ranksolo=ranksolo,
                rank5=rank5,
                win=win,
                champ=_champ,
                img=img
            )