from riotwatcher import LolWatcher, ApiError
import os

lol_watcher = LolWatcher(os.getenv('RIOT_API_KEY'))

my_region = 'na1'

me = lol_watcher.summoner.by_name(my_region, 'Jareco')
print(me)

# all objects are returned (by default) as a dict
my_ranked_stats = lol_watcher.league.by_summoner(my_region, me['id'])
print(my_ranked_stats)

versions = lol_watcher.data_dragon.versions_for_region(my_region)
champions_version = versions['n']['champion']

current_champ_list = lol_watcher.data_dragon.champions(champions_version)
print(current_champ_list)


try:
    response = lol_watcher.summoner.by_name(my_region, 'Jareco')
except ApiError as err:
    if err.response.status_code == 429:
        print('We should retry in {} seconds.'.format(err.headers['Retry-After']))
        print('this retry-after is handled by default by the RiotWatcher library')
        print('future requests wait until the retry-after time passes')
    elif err.response.status_code == 404:
        print('Summoner with that ridiculous name not found.')
    else:
        raise
'''
import cassiopeia as cass
import os
from dotenv import load_dotenv

class Summon:
    def __init__(self, name):
        cass.set_riot_api_key(os.getenv('RIOT_API_KEY'))
        cass.set_default_region('NA')
        self.real = True
        try:
            self.summoner = cass.Summoner(name=name)
        except:
            self.real = False
        #for match in self.summoner.match_history(begin_index=0, end_index=9):
        #    self.match_history.append(match.)


    def get_real(self):
        return self.real
    def get_name(self) -> str:
        return self.summoner.name
    def get_icon(self):
        return self.summoner.profile_icon
    def get_mh(self):
        return self.summoner.match_history(begin_index=0, end_index=9)
    def get_level(self) -> str:
        return self.summoner.level
'''