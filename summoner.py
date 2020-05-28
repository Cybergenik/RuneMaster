import dotenv
dotenv.load_dotenv()

import os
from riotwatcher import LolWatcher, ApiError

RIOT_API_KEY = os.getenv("RIOT_API_KEY")

lol_watcher = LolWatcher(RIOT_API_KEY)
my_region = 'NA1'

class Summon:
    def __init__(self, name):
        try:
            self.player_info = lol_watcher.summoner.by_name(my_region, name)
            self.player_stats = lol_watcher.league.by_summoner(my_region, self.player_info['id'])
            self.real_player = True

        except ApiError as err:
            if err.response.status_code == 429:
                print('We should retry in {} seconds.'.format(err.headers['Retry-After']))
                print('this retry-after is handled by default by the RiotWatcher library')
                print('future requests wait until the retry-after time passes')
            elif err.response.status_code == 404:
                print('Summoner with that ridiculous name not found.')
            else:
                raise

    def get_real_player(self):
        return self.real_player
    def get_player_info(self):
        return self.player_info
    def get_player_stats(self):
        return self.player_stats