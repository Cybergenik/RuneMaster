import os
import discord
from discord.ext import commands
import re
import json
import requests
from driver import get_driver
from dotenv import load_dotenv
from champs import Champ
from summoner import Summon
from screenshot import Screenshot

load_dotenv()

if os.getenv('DISCORD_TOKEN') != None:
    client = discord.Client()
    bot = commands.Bot(command_prefix='>')
else:
    raise EnvironmentError("DISCORD_TOKEN env variable is not set")

# Global Variable declaration
with open('bot/tiers.json') as f:
    TIERS = json.load(f)
with open('bot/regions.json') as f:
    REGIONS = json.load(f)
with open('bot/commands.json') as f:
    COMMANDS = json.load(f)
VERSION = requests.get('https://ddragon.leagueoflegends.com/api/versions.json').json()[0]
CHAMPS = requests.get(f'https://ddragon.leagueoflegends.com/cdn/{VERSION}/data/en_US/champion.json').json()['data']

def real_champ(name):
    _name = name.lower().replace(' ', '')
    for champ in CHAMPS:
        if champ.lower() == _name:
            return champ
    return None

def real_region(region):
    for prefix in REGIONS:
        if REGIONS[prefix] == region.lower():
            return prefix
    return None

def clean_temp(temp):
    for f in temp:
        if f.endswith('.png'):
            os.remove(f'temp/{f}')

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    print (f'{client.user} is connected to the following guilds:\n')
    for guild in client.guilds:
        print(f'{guild.name}(id: {guild.id})\n')
    print(f'League of Legends Version {VERSION}')

@client.event
async def on_message(message):
    temp = os.listdir('temp/')
    if len(temp) >= 20:
        await message.channel.send('Self cleaning, please wait...')
        print("cleaning temp dir...")
        clean_temp(temp=temp)
        get_driver().reset()
        print('Finished clearing cache and driver restarted')
        await message.channel.send('RuneMaster Ready to go!')
        return
    if message.author == client.user:
        return
    if re.search('^>>> ', message.content, flags=re.IGNORECASE):
        return
    if re.search('^> ', message.content, flags=re.IGNORECASE):
        return
    if re.search('Runemaster', message.content, flags=re.IGNORECASE):
        await message.channel.send('Ready for the Rift? type >commands for a list of all commands')
        return
#region Generic commands
    if re.search('^>hello', message.content, flags=re.IGNORECASE):
        await message.channel.send('Hello Summoner')
        return
    if re.search('^>commands', message.content, flags=re.IGNORECASE):
        response = discord.Embed(
            title =  "__Runemaster Commands__",
            description = "All commands start with a `>` and most commands will require an argument, usually this will be the name of a champion. If the champ has a space or a singlequote dont include them in the name. ex: DrMundo, Reksai",
        )
        for command in COMMANDS.values():
            response.add_field(name=command['usage'], value=command['value'], inline=False)
        await message.channel.send(embed=response)
        return       
    if re.search('^>regions', message.content, flags=re.IGNORECASE):
        desc = '\n'.join(REGIONS.values())
        response = discord.Embed(
            title =  "__Regions__",
            description = desc
        )
        await message.channel.send(embed=response)
        return
    if re.search('^>tierlist|^>tiers', message.content, flags=re.IGNORECASE): 
        file = discord.File('images/tierlist.png', filename='tierlist.png')
        await message.channel.send(f"__Ranked Tier List__",file=file)
        return
    if re.search('^>oldtierlist|^>oldtiers', message.content, flags=re.IGNORECASE):
        file = discord.File('images/old_tierlist.png', filename='old_tierlist.png')
        await message.channel.send(f"__Old Ranked Tier List__",file=file)
        return
    if re.search('^>reload', message.content, flags=re.IGNORECASE):
        await message.channel.send("Reloading RuneMaster...")
        get_driver().reset()
        await message.channel.send("RuneMaster Ready to go!")
        return
#endregion
    if re.search('^>', message.content):
        _in = message.content.split(' ', 1)
        command = _in[0].lower()
        if len(_in) == 1:
            await message.channel.send('Type `>commands` for a list of commands and how to use them.')
            return
        else:
            args = _in[1].lower().strip()

        if command == '>help':
            for command in COMMANDS:
                if args.lower() == command:
                    response = discord.Embed(
                        title =  f"__{command.capitalize()} Help__",
                        description = f"{COMMANDS[command]['usage']} \n {COMMANDS[command]['value']}",
                    )   
                    await message.channel.send(embed=response)
                    return
            await message.channel.send("Command doesn't exist, type *>commands* for a list of commands")

#region Champion related commands
        elif command == '>info':
            champ = real_champ(name=args)
            if champ is not None:
                info = Champ(champ=champ, champs=CHAMPS, version=VERSION)
                response = discord.Embed(
                    title =  f"__{info.champ} | {info.title}__",
                    description = info.desc,
                    url=info.url
                )
                response.set_image(url=info.img)
                response.add_field(name="Tags", value= info.tags, inline=False)
                response.add_field(name="Stats", value= info.stats, inline=False)
                await message.channel.send(embed=response)
            elif champ is None:
                await message.channel.send("That champ does not exist")

        elif command == '>runes':
            await message.channel.send("Fetching Rune Data...")
            if real_champ(name=args) is not None:
                info = Screenshot(name=args)
                seed = info.runes()
                file = discord.File(f'temp/{seed}.png', filename=f'{seed}.png')
                await message.channel.send(f"__{args.capitalize()} Runes__",file=file)
            else:
                await message.channel.send("That champ does not exist")

        elif command == '>build':
            await message.channel.send("Fetching Build Data...") 
            if real_champ(name=args) is not None:
                info = Screenshot(name=args)
                seed = info.build()
                file = discord.File(f'temp/{seed}.png', filename=f'{seed}.png')
                await message.channel.send(f"__{args.capitalize()} Build__",file=file)
            else:
                await message.channel.send("That champ does not exist")

        elif command == '>skills':
            await message.channel.send("Fetching Skills Data...") 
            if real_champ(name=args) is not None:
                info = Screenshot(name=args)
                seed = info.skills()
                file = discord.File(f'temp/{seed}.png', filename=f'{seed}.png')
                await message.channel.send(f"__{args.capitalize()} Skills__",file=file)
            else:
                await message.channel.send("That champ does not exist")

        elif command == '>stats':
            await message.channel.send("Fetching Stats Data...") 
            if real_champ(name=args) is not None:
                info = Screenshot(name=args)
                seed = info.champ_stats()
                file = discord.File(f'temp/{seed}.png', filename=f'{seed}.png')
                await message.channel.send(f"__{args.capitalize()} Stats__",file=file)
            else:
                await message.channel.send("That champ does not exist")

        elif command == '>sums':
            await message.channel.send("Fetching Summoner Spell data...") 
            if real_champ(name=args) is not None:
                info = Screenshot(name=args)
                seed = info.sums()
                file = discord.File(f'temp/{seed}.png', filename=f'{seed}.png')
                await message.channel.send(f"__{args.capitalize()} Summoner Spells__",file=file)
            else:
                await message.channel.send("That champ does not exist")

        elif command == '>matchups':
            await message.channel.send("Fetching Matchup data...") 
            if real_champ(name=args) is not None:
                info = Screenshot(name=args)
                seed = info.matchups()
                file = discord.File(f'temp/{seed}.png', filename=f'{seed}.png')
                await message.channel.send(f"__{args.capitalize()} Matchups__",file=file)
            else:
                await message.channel.send("That champ does not exist")
#endregion
        
        elif command == '>tier':
            if args in TIERS:
                file = discord.File(TIERS[args], filename=f'args.png')
                await message.channel.send(f"__{args.capitalize()}__",file=file)
            else:
                await message.channel.send("That ranked tier does not exist")

#region Summoner related commands
        elif command == '>summon':
            await message.channel.send("Fetching Summoner data...")
            args = args.split(" ", 1)
            if len(args) > 1:
                prefix = real_region(region=args[0])
                if prefix is not None:
                    player = Summon(name=args[1], region=args[0], prefix=prefix)
                else:
                    await message.channel.send("Region does not exist, type *>regions* for a list of regions")
            else:
                player = Summon(name=args[0])
            if player.real_player:
                response = discord.Embed(
                    title =  f"__{player.name}__" , 
                    url= player.url
                    )
                response.set_thumbnail(url=f"https://ddragon.leagueoflegends.com/cdn/10.10.3216176/img/profileicon/{player.icon}.png")
                response.add_field(name="Level:", value=player.level, inline=False)
                response.add_field(name="Solo/Duo Rank:", value=player.ranksolo, inline=False)
                if player.rank5 != None:
                    response.add_field(name="5v5 Flex Rank: ", value=player.rank5, inline=False)
                response.add_field(name="Ranked Season Win %:", value=f'{player.win}', inline=True)
                response.add_field(name="Highest Mastery :", value=player.champ, inline=False)
                response.set_image(url=player.img)
                await message.channel.send(embed=response)
            else:
                await message.channel.send("That Summoner does not exist or is on a different region")

        elif command == '>history':
            await message.channel.send("Fetching Player History data...")
            args = args.split(" ", 1)
            if len(args) > 1:
                prefix = real_region(region=args[0])
                if prefix is not None:
                    player = Screenshot(name=args[1], prefix=prefix)
                else:
                    await message.channel.send("Region does not exist, type *>regions* for a list of regions")
            else:
                player = Screenshot(name=args[0], prefix='na')
            try:
                seed = player.get_matches()
                file = discord.File(f'temp/{seed}.png', filename=f'runes{seed}.png')
                await message.channel.send(f'__{player.name} Match History__',file=file)
            except Exception as e:
                print(e)
                await message.channel.send("That Summoner does not exist")
        else:
            await message.channel.send('Type `>commands` for a list of commands and how to use them.')
#endregion
client.run(os.getenv('DISCORD_TOKEN'))
