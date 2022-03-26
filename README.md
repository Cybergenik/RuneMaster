Runemaster
====
<a href="https://discord.com/api/oauth2/authorize?client_id=713831642061602827&permissions=523328&scope=bot" target="_blank"><img src="images/default.png" alt="Runemaster Icon" width="256" height="256"/></a>
===
A Discord bot for League of Legends! Runemaster is a minimal bot that gives fast and reliable Player, Champion, and Ranking data for League of Legends. It is secure, uses minimal permissions, and is automatically updated to the newest patch.
## **Commands**

*All commands start with a* `>` *and most commands will require an argument, usually this will be the name of a champion. If the champ has a* **space** *or a* **singlequote** *dont include them in the name. ex: DrMundo, Reksai, Kaisa*

#### Info

- <kbd>>hello</kbd>: RuneMaster greets you!
- <kbd>>commands</kbd>: Returns a list of all the commands
- <kbd>>help *</kbd>: Returns a tooltip with the usage on a specific command `>help info`
- <kbd>>tierlist | tiers</kbd>: Returns an image of the current up to date ranked tier list
- <kbd>>oldtierlist | oldtiers</kbd>: Returns an image of the old outdated ranked tier list
- <kbd>>tier *</kbd>: Returns an image of the tier rank specified `>tier gold`
- <kbd>>regions</kbd>: Returns a list of all regions that you can use to look up 

#### Player

*all of these commands take the name of a player as an arguement(input)* **`>summon KR hideonbush`** 

- <kbd>>summon *</kbd>: Returns information on a Summoner like they're level, rank, player icon. Default region is NA, don't include a region if you just want NA
- <kbd>>matches *</kbd>: Returns an image of the last 10 games in the players entire match history 
- <kbd>>soloranked_matches *</kbd>: Returns an image of the last 10 games in the players solo ranked match history 
- <kbd>>flexranked_matches *</kbd>: Returns an image of the last 10 games in the players flex ranked match history 

#### Champion

*all of these commands take the name of a champion as an arguement(input)* **`>info Aatrox`**

- <kbd>>info *</kbd>: Returns detailed information on a Champion, including description, stats, image
- <kbd>>runes *</kbd>: Returns an image of the highest win-rate Runes on that champion
- <kbd>>build *</kbd>: Returns an image of the highest win-rate Build on that champion
- <kbd>>skills</kbd>, <kbd>>abilities</kbd>, <kbd>>spells</kbd>: Returns an image of Summoner Spells, Pick and Win Rate, as well as skill-up order.
- <kbd>>stats *</kbd>: Returns an image of important stats about the champion like Tier, Abilities, and Champions that counter this champion. 

## Development

*I accept pull requests! if you think it'll make it faster or better, submit a PR :>*

### **installation**

- From source:
    1. `git clone https://github.com/Cybergenik/RuneMaster`
    2. `cd RuneMaster`
    3. `pip install -r requirements`
    4. `playwright install chromium`
    5. `python bot/runemaster.py`

### **Requirements**
#### Packages:
        - Python 3.9
        - playwright 
        - requests
        - discord
        - python-dotenv
        - [riotwatcher](https://github.com/pseudonym117/Riot-Watcher)

#### Enviornment Variables:
        Sample .env:
            DISCORD_TOKEN=1234
            RIOT_API_KEY=1234
