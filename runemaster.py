import os
import discord
import re
import json
from champs import Champ
from champs import Screenshots
from summoner import Summon

TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()

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
        with open('commands.json') as f:
            commands = json.load(f)
        for command in commands:
            response.add_field(name=commands[command]['usage'], value=commands[command]['value'], inline=False)
        await message.channel.send(embed=response)
        return
    elif re.search('^>regions', message.content, flags=re.IGNORECASE):
        info = Summon()
        desc = []
        for region in info.get_regions():
            desc.append(f'{region} \n ')
        response = discord.Embed(
            title =  "__Regions__",
            description = desc,
        )
        response.set_footer("RuneMaster 2020")
        await message.channel.send(embed=response)

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
                    title =  "__"+info.get_champ()+" | "+info.get_title()+"__",
                    description = info.get_desc(),
                )
                response.set_image(url=info.get_img())
                response.add_field(name="Tags", value= info.get_tags(), inline=False)
                response.add_field(name="Stats", value= info.get_stats(), inline=False)
                response.set_footer("RuneMaster 2020")
                await message.channel.send(embed=response)
            else:
                await message.channel.send("That champ does not exist")
            return

        elif command == '>runes':
            info = Screenshots(_args)
            if info.get_real():
                await message.channel.send("Fetching Rune Data...") 
                seed = info.runes()
                file = discord.File('./images/vape'+seed+'.png', filename='runes'+seed+'.png')
                await message.channel.send("__"+_args.capitalize()+" Runes__",file=file)
                info.kill_seed(seed)
            else:
                await message.channel.send("That champ does not exist")
            return

        elif command == '>build':
            info = Screenshots(_args)
            if info.get_real():
                await message.channel.send("Fetching Build Data...") 
                seed = info.build()
                file = discord.File('./images/vape'+seed+'.png', filename='runes'+seed+'.png')
                await message.channel.send("__"+_args.capitalize()+" Build__",file=file)
                info.kill_seed(seed)
            else:
                await message.channel.send("That champ does not exist")
            return

        elif command == '>skills':
            info = Screenshots(_args)
            if info.get_real():
                await message.channel.send("Fetching Skills Data...") 
                seed = info.skills()
                file = discord.File('./images/vape'+seed+'.png', filename='runes'+seed+'.png')
                await message.channel.send("__"+_args.capitalize()+" Skill Order__",file=file)
                info.kill_seed(seed)
            else:
                await message.channel.send("That champ does not exist")
            return

        elif command == '>stats':
            info = Screenshots(_args)
            if info.get_real():
                await message.channel.send("Fetching Stats Data...") 
                seed = info.stats()
                file = discord.File('./images/vape'+seed+'.png', filename='runes'+seed+'.png')
                await message.channel.send("__"+_args.capitalize()+" Stats__",file=file)
                info.kill_seed(seed)
            else:
                await message.channel.send("That champ does not exist")
            return

        elif command == '>sums':
            info = Screenshots(_args)
            if info.get_real():
                await message.channel.send("Fetching Summoner Spell data...") 
                seed = info.sums()
                file = discord.File('./images/vape'+seed+'.png', filename='runes'+seed+'.png')
                await message.channel.send("__"+_args.capitalize()+" Summoners__",file=file)
                info.kill_seed(seed)
            else:
                await message.channel.send("That champ does not exist")
            return

        elif command == '>matchups':
            info = Screenshots(_args)
            if info.get_real():
                await message.channel.send("Fetching Matchup data...") 
                seed = info.matchups()
                file = discord.File('./images/vape'+seed+'.png', filename='runes'+seed+'.png')
                await message.channel.send("__"+_args.capitalize()+" Summoners__",file=file)
                info.kill_seed(seed)
            else:
                await message.channel.send("That champ does not exist")
            return

        elif command == '>summon':
            _in = _args.split(' ', 1)
            if _in.length() == 1:
                info = Summon(_in[0])
            elif _in.length() == 2:
                info = Summon(_in[0], _in[1])
            else:
                await message.channel.send('Type `>help` for a list of commands and how to use them.')

            if info.get_real_player():
                seed = info.get_match_info()
                file = discord.File('./images/vape'+seed+'.png', filename='runes'+seed+'.png')

                response = discord.Embed(
                    title =  f"__{info.get_name()}__" , 
                    url=f"https://na.op.gg/summoner/userName={info.get_name()}"
                    )
                response.set_thumbnail(url=f"https://ddragon.leagueoflegends.com/cdn/10.10.3216176/img/profileicon/{info.get_icon()}.png")
                response.add_field(name="Level:", value=info.get_level(), inline=False)
                response.add_field(name="Rank:", value=info.get_rank(), inline=False)
                response.add_field(name="Overall Win %:", value=info.get_win(), inline=False)
                response.set_footer(text="RuneMaster 2020")

                await message.channel.send(embed=response)
                await message.channel.send(file=file)
                info.kill_seed(seed)
            else:
                await message.channel.send("That Summoner does not exist")
            return

        elif command == '>history':
            _in = _args.split(' ', 1)
            if _in.length() == 1:
                info = Summon(_in[0])
            elif _in.length() == 2:
                info = Summon(_in[0], _in[1])
            else:
                await message.channel.send('Type `>help` for a list of commands and how to use them.')

            if info.get_real_player():
                seed = info.get_matches()
                file = discord.File('./images/vape'+seed+'.png', filename='runes'+seed+'.png') 
                await message.channel.send(f'__{info.get_name()} Match History__',file=file)
                info.kill_seed(seed)
            else:
                await message.channel.send("That Summoner does not exist")
            return

client.run(TOKEN)