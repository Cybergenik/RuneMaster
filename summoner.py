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
        self.match_history = {}
        for match in self.summoner.match_history(begin_index=0, end_index=9):
            self.match_history.append(match.)


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
