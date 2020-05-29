import os
from riotwatcher import LolWatcher

RIOT_API_KEY = os.getenv("RIOT_API_KEY")
lol_watcher = LolWatcher(RIOT_API_KEY)

player_info = lol_watcher.summoner.by_name("kr", "INSECTSLIFE")
print(player_info)
player_stats = lol_watcher.league.by_summoner("kr", player_info['id'])
print(player_stats)