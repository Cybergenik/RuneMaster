from bot.utils import CHAMPS, VERSION

class Champ:
    def __init__(self, champ):
        self.champ = CHAMPS[champ]['id']
        self.title = CHAMPS[self.champ]['title']
        self.img = f"https://ddragon.leagueoflegends.com/cdn/{VERSION}/img/champion/{CHAMPS[self.champ]['image']['full']}"
        self.desc =  CHAMPS[self.champ]['blurb']
        self.tags = ' '.join(CHAMPS[self.champ]['tags'])
        self.stats = f'Health: {CHAMPS[self.champ]["stats"]["hp"]} \n \
                    Move Speed: {CHAMPS[self.champ]["stats"]["movespeed"]} \n \
                    Attack Damage: {CHAMPS[self.champ]["stats"]["attackdamage"]} \n \
                    Attack Range: {CHAMPS[self.champ]["stats"]["attackrange"]} \n \
                    Attack Speed: {CHAMPS[self.champ]["stats"]["attackspeed"]}'
        self.url = f'https://www.op.gg/champion/{self.champ}/statistics'
        self.real = True 
        self.name = CHAMPS[champ]['name']
                
