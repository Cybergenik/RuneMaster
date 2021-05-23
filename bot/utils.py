import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

# Global Variable declaration
with open('bot/tiers.json') as f:
    TIERS = json.load(f)
with open('bot/regions.json') as f:
    REGIONS = json.load(f)
with open('bot/commands.json') as f:
    COMMANDS = json.load(f)
VERSION = requests.get('https://ddragon.leagueoflegends.com/api/versions.json').json()[0]
CHAMPS = requests.get(f'https://ddragon.leagueoflegends.com/cdn/{VERSION}/data/en_US/champion.json').json()['data']

TOKEN = os.getenv('DISCORD_TOKEN')
if TOKEN is None:
    raise EnvironmentError("DISCORD_TOKEN env variable is not set")

RIOT_API_KEY = os.getenv("RIOT_API_KEY")
if RIOT_API_KEY is None:
    raise EnvironmentError("RIOT_API_KEY env variable is not set")

def real_champ(name):
    _name = name.lower().replace(' ', '')
    for champ in CHAMPS:
        if champ.lower() == _name:
            return champ
    return None

def real_region(region):
    return region.lower() in REGIONS