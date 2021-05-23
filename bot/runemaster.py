import re
from discord import Client, Embed, File
from bot.screenshot import get_screenshot
from bot.champs import Champ
from bot.summoner import Summon
from bot.utils import TOKEN, VERSION, COMMANDS, REGIONS, TIERS, real_champ, real_region


client = Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    print (f'{client.user} is connected to the following guilds:\n')
    for guild in client.guilds:
        print(f'{guild.name}(id: {guild.id})\n')
    print(f'League of Legends Version {VERSION}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if re.search('^>>> ', message.content, flags=re.IGNORECASE):
        return
    if re.search('^> ', message.content, flags=re.IGNORECASE):
        return
    if re.search('@RuneMaster', message.content):
        await message.channel.send('Ready for the Rift? type >commands for a list of all commands')
        return
#region Generic commands
    if re.search('^>hello', message.content, flags=re.IGNORECASE):
        await message.channel.send('Hello Summoner')
        return
    if re.search('^>commands', message.content, flags=re.IGNORECASE):
        response = Embed(
            title =  "__Runemaster Commands__",
            description = "All commands start with a `>` and most commands will require an argument, usually this will be the name of a champion. If the champ has a space or a singlequote dont include them in the name. ex: DrMundo, Reksai",
        )
        for command in COMMANDS.values():
            response.add_field(name=command['usage'], value=command['value'], inline=False)
        await message.channel.send(embed=response)
        return       
    if re.search('^>regions', message.content, flags=re.IGNORECASE):
        desc = '\n'.join(REGIONS.values())
        response = Embed(
            title =  "__Regions__",
            description = desc
        )
        await message.channel.send(embed=response)
        return
    if re.search('^>tierlist|^>tiers', message.content, flags=re.IGNORECASE): 
        file = File('images/tierlist.png', filename='tierlist.png')
        await message.channel.send(f"__Ranked Tier List__",file=file)
        return
    if re.search('^>oldtierlist|^>oldtiers', message.content, flags=re.IGNORECASE):
        file = File('images/old_tierlist.png', filename='old_tierlist.png')
        await message.channel.send(f"__Old Ranked Tier List__",file=file)
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
                    response = Embed(
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
                info = Champ(champ=champ)
                response = Embed(
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
            name = real_champ(name=args)
            if name is not None:
                file = File(fp=await get_screenshot(name=name, action="runes"), filename=f'{name}.png')
                await message.channel.send(f"__{args.capitalize()} Runes__",file=file)
            else:
                await message.channel.send("That champ does not exist")

        elif command == '>build':
            await message.channel.send("Fetching Build Data...") 
            name = real_champ(name=args)
            if name is not None:
                file = File(fp=await get_screenshot(name=name, action="build"), filename=f'{name}.png')
                await message.channel.send(f"__{args.capitalize()} Build__",file=file)
            else:
                await message.channel.send("That champ does not exist")

        elif command == '>skills' or command == '>abilities' or command == ">spells":
            await message.channel.send("Fetching Skills Data...") 
            name = real_champ(name=args)
            if name is not None:
                file = File(fp=await get_screenshot(name=name, action="skills"), filename=f'{name}.png')
                await message.channel.send(f"__{args.capitalize()} Skills__",file=file)
            else:
                await message.channel.send("That champ does not exist")

        elif command == '>stats':
            await message.channel.send("Fetching Stats Data...") 
            name = real_champ(name=args)
            if name is not None:
                file = File(fp=await get_screenshot(name=name, action="stats"), filename=f'{name}.png')
                await message.channel.send(f"__{args.capitalize()} Stats__",file=file)
            else:
                await message.channel.send("That champ does not exist")
#endregion
        
        elif command == '>tier':
            if args in TIERS:
                file = File(TIERS[args], filename=f'args.png')
                await message.channel.send(f"__{args.capitalize()}__",file=file)
            else:
                await message.channel.send("That ranked tier does not exist")

#region Summoner related commands
        elif command == '>summon':
            await message.channel.send("Fetching Summoner data...")
            args = args.split(" ", 1)
            if len(args) > 1:
                reg = args[0].lower()
                if real_region(region=reg):
                    player = Summon(name=args[1], region=REGIONS[reg], prefix=reg)
                else:
                    await message.channel.send("Region does not exist, type *>regions* for a list of regions")
            else:
                player = Summon(name=args[0])
            if player.real_player:
                response = Embed(
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

        elif "matches" in command:
            await message.channel.send("Fetching Player Match data...")
            args = args.split(" ", 1)
            if len(args) > 1:
                reg = args[0].lower()
                name = args[1]
                if not real_region(region=reg):
                    await message.channel.send("Region does not exist, type *>regions* for a list of regions")
                    return
            else:
                reg = "na"
                name = args[0]
            if command == ">soloranked_matches":   action = "soloranked_matches"
            elif command == ">flexranked_matches": action = "flexranked_matches"
            elif command == ">matches":            action = "matches"
            try:
                file = File(fp=await get_screenshot(name=args[0], action=action, prefix=reg), filename=f'{args[0]}.png')
                await message.channel.send(f'__{args[0]} Match History__',file=file)
            except Exception as e:
                print(e)
                await message.channel.send("That Summoner does not exist")
        else:
            await message.channel.send('Type `>commands` for a list of commands and how to use them.')
#endregion
client.run(TOKEN)
