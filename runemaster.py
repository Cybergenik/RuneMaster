import os
import discord
import re
from champs import Champ
from screenshots import Screenshots
import json
import sys
#from summoner import Summon
print(os.getenv('DISCORD_TOKEN'))
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

    if re.search('^>', message.content):
        _in = message.content.split(' ', 1)
        command = _in[0].lower()
        try:
            _args = _in[1].replace(" ", "").lower()
        except:
            await message.channel.send('Type `>help` for a list of commands and how to use them.')
            return
        if command == '>info':
            info = Champ(_args)
            if info.get_real():
                response = discord.Embed(
                    title =  "__"+info.get_champ()+" | "+info.get_title()+"__",
                    description = info.get_desc(),
                    footer = "RuneMaster 2020"
                )
                response.set_image(url=info.get_img())
                response.add_field(name="Tags", value= info.get_tags(), inline=False)
                response.add_field(name="Stats", value= info.get_stats(), inline=False)
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
            
        '''
        elif command == '>summon':
            info = Summon(_args)
            if info.get_real():
                response = discord.Embed(
                    title =  "__"+info.get_name()+"__",
                    description = info.get_level(),
                    footer = "RuneMaster 2020"
                )
                response.add_field(name="Icon", value="placeholder", inline=False)
                await message.channel.send(embed=response)
            else:
                await message.channel.send("That Summoner does not exist")
            return
        '''
client.run(TOKEN)