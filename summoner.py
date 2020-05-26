import cassiopeia as cass
import os
from dotenv import load_dotenv

class Summon:
    def __init__(self, name):
        load_dotenv()
        cass.set_riot_api_key(os.getenv('RIOT_API_KEY'))
        cass.set_default_region('NA')
        self.real = True
        try:
            self.summoner = cass.get_summoner(name=name)
        except:
            self.real = False

    def get_real(self):
        return self.real
    def get_icon(self):
        return self.summoner.profile_icon
    def get_shit(self):
        return self.summoner.load
    def get_level(self) -> str:
        return self.summoner.level
