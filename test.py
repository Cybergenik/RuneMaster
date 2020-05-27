import cassiopeia as cass
import os

cass.set_riot_api_key(os.getenv('RIOT_API_KEY'))
cass.set_default_region('NA')

summoner = cass.Summoner(name="Jareco")
matches = summoner.match_history(begin_index=0, end_index=9)

for i in matches:
    print(type(i))