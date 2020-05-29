import os
import discord
import re
import json
from champs import Champ
from champs import Screenshots
from summoner import Summon

TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()

with open('tiers.json') as f:
    TIERS = json.load(f)
with open('regions.json') as f:
    REGIONS = json.load(f)
with open('commands.json') as f:
    COMMANDS = json.load(f)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    print (f'{client.user} is connected to the following guilds:\n')
    for guild in client.guilds:
        print(
            f'{guild.name}(id: {guild.id})\n'
        )

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    elif re.search('^>hello', message.content, flags=re.IGNORECASE):
        await message.channel.send('Hello Summoner')
        return
    elif re.search('^>help', message.content, flags=re.IGNORECASE):
        response = discord.Embed(
            title =  "__Runemaster | Help__",
            description = "All commands start with a `>` and most commands will require an argument, usually this will be the name of a champion. ",
            footer = "RuneMaster 2020"
        )
        for command in COMMANDS:
            response.add_field(name=COMMANDS[command]['usage'], value=COMMANDS[command]['value'], inline=False)
        await message.channel.send(embed=response)
        return
    elif re.search('^>regions', message.content, flags=re.IGNORECASE):
        desc = ''
        for region in REGIONS:
            desc = f'{desc} {REGIONS[region].upper()} \n '
        response = discord.Embed(
            title =  "__Regions__",
            description = desc
        )
        await message.channel.send(embed=response)
        return
    elif re.search('^>tierlist', message.content, flags=re.IGNORECASE): 
        file = discord.File('./images/tierlist.png', filename='tierlist.png')
        await message.channel.send(f"__Ranked Tier List__",file=file)
        return
    elif re.search('^>old_tierlist', message.content, flags=re.IGNORECASE):
        file = discord.File('./images/old_tierlist.png', filename='old_tierlist.png')
        await message.channel.send(f"__Old Ranked Tier List__",file=file)
        return

    if re.search('^>', message.content):
        _in = message.content.split(' ', 1)
        command = _in[0].lower()
        try:
            _args = _in[1].lower()
        except:
            await message.channel.send('Type `>help` for a list of commands and how to use them.')
            return
        if command == '>info':
            info = Champ(_args)
            if info.get_real():
                response = discord.Embed(
                    title =  f"__{info.get_champ()} | {info.get_title()}__",
                    description = info.get_desc(),
                )
                response.set_image(url=info.get_img())
                response.add_field(name="Tags", value= info.get_tags(), inline=False)
                response.add_field(name="Stats", value= info.get_stats(), inline=False)
                response.image
                await message.channel.send(embed=response)
            else:
                await message.channel.send("That champ does not exist")
            return

        elif command == '>runes':
            info = Screenshots(_args)
            if info.get_real():
                await message.channel.send("Fetching Rune Data...") 
                seed = info.runes()
                file = discord.File(f'./images/vape{seed}.png', filename=f'runes{seed}.png')
                await message.channel.send(f"__{_args.capitalize()} Runes__",file=file)
                info.kill_seed(seed)
                info.kill_driver()
            else:
                await message.channel.send("That champ does not exist")
            return

        elif command == '>build':
            info = Screenshots(_args)
            if info.get_real():
                await message.channel.send("Fetching Build Data...") 
                seed = info.build()
                file = discord.File(f'./images/vape{seed}.png', filename=f'runes{seed}.png')
                await message.channel.send(f"__{_args.capitalize()} Build__",file=file)
                info.kill_seed(seed)
                info.kill_driver()
            else:
                await message.channel.send("That champ does not exist")
            return

        elif command == '>skills':
            info = Screenshots(_args)
            if info.get_real():
                await message.channel.send("Fetching Skills Data...") 
                seed = info.skills()
                file = discord.File(f'./images/vape{seed}.png', filename='runes{seed}.png')
                await message.channel.send(f"__{_args.capitalize()} Skill Order__",file=file)
                info.kill_seed(seed)
                info.kill_driver()
            else:
                await message.channel.send("That champ does not exist")
            return

        elif command == '>stats':
            info = Screenshots(_args)
            if info.get_real():
                await message.channel.send("Fetching Stats Data...") 
                seed = info.stats()
                file = discord.File(f'./images/vape{seed}.png', filename=f'runes{seed}.png')
                await message.channel.send(f"__{_args.capitalize()} Stats__",file=file)
                info.kill_seed(seed)
                info.kill_driver()
            else:
                await message.channel.send("That champ does not exist")
            return

        elif command == '>sums':
            info = Screenshots(_args)
            if info.get_real():
                await message.channel.send("Fetching Summoner Spell data...") 
                seed = info.sums()
                file = discord.File(f'./images/vape{seed}.png', filename=f'runes{seed}.png')
                await message.channel.send(f"__{_args.capitalize()} Summoners__",file=file)
                info.kill_seed(seed)
                info.kill_driver()
            else:
                await message.channel.send("That champ does not exist")
            return

        elif command == '>matchups':
            info = Screenshots(_args)
            if info.get_real():
                await message.channel.send("Fetching Matchup data...") 
                seed = info.matchups()
                file = discord.File(f'./images/vape{seed}.png', filename=f'runes{seed}.png')
                await message.channel.send(f"__{_args.capitalize()} Summoners__",file=file)
                info.kill_seed(seed)
                info.kill_driver()
            else:
                await message.channel.send("That champ does not exist")
            return

        elif command == '>summon':
            _in = _args.split(' ', 1)
            if len(_in) == 1:
                info = Summon(name=_in[0])
            elif len(_in) == 2:
                info = Summon(region=_in[0], name=_in[1])
            if info.get_real_player():
                response = discord.Embed(
                    title =  f"__{info.get_name()}__" , 
                    url= info.get_url()
                    )
                response.set_thumbnail(url=f"https://ddragon.leagueoflegends.com/cdn/10.10.3216176/img/profileicon/{info.get_icon()}.png")
                response.add_field(name="Level:", value=info.get_level(), inline=False)
                response.add_field(name="Rank:", value=info.get_rank(), inline=False)
                response.add_field(name="Overall Win %:", value=info.get_win(), inline=False)
                await message.channel.send(embed=response)
            else:
                await message.channel.send("That Summoner does not exist or the region is incorrect")
            return

        elif command == '>history':
            _in = _args.split(' ', 1)
            if len(_in) == 1:
                info = Summon(name=_in[0], ss=True)
            elif len(_in) == 2:
                info = Summon(region=_in[0], name=_in[1], ss=True)
            if info.get_real_player():
                seed = info.get_match_info()
                seed2 = info.get_matches()
                file = discord.File(f'./images/vape{seed}.png', filename=f'runes{seed}.png')
                file2 = discord.File(f'./images/vape{seed2}.png', filename=f'runes{seed2}.png')
                await message.channel.send(f'__{info.get_name()} Match History__',file=file)
                await message.channel.send(file=file2)
                info.kill_seed(seed)
                info.kill_seed(seed2)
                info.kill_driver()
            else:
                await message.channel.send("That Summoner does not exist or the region is incorrect!")
            return
        elif command == '>tier':
            if _args in TIERS:
                file = discord.File(TIERS[_args], filename=f'_args.png')
                await message.channel.send(f"__{_args.capitalize()}__",file=file)
            else:
                await message.channel.send("That ranked tier does not exist")
            return 

client.run(TOKEN)