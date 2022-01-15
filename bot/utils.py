import os
import json
import requests
from dotenv import load_dotenv
from cachetools.func import ttl_cache

load_dotenv()

# Global Variable declaration
with open('bot/tiers.json') as f:
    TIERS = json.load(f)
with open('bot/regions.json') as f:
    REGIONS = json.load(f)
with open('bot/commands.json') as f:
    COMMANDS = json.load(f)

@ttl_cache(maxsize=1, ttl=86400) # 86400 : 24 hours
def get_version() -> str:
    return requests.get('https://ddragon.leagueoflegends.com/api/versions.json').json()[0]

@ttl_cache(maxsize=1, ttl=86400) # 86400 : 24 hours
def get_champs() -> list:
    return requests.get(f'https://ddragon.leagueoflegends.com/cdn/{get_version()}/data/en_US/champion.json').json()['data']

TOKEN = os.getenv('DISCORD_TOKEN')
if TOKEN is None:
    raise EnvironmentError("DISCORD_TOKEN env variable is not set")

RIOT_API_KEY = os.getenv("RIOT_API_KEY")
if RIOT_API_KEY is None:
    raise EnvironmentError("RIOT_API_KEY env variable is not set")

def real_region(region):
    return region.lower() in REGIONS
