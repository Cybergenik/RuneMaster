from dataclasses import dataclass
from bot.utils import get_version, get_champs

@dataclass
class Champ:
    """Model for representing a League of Legends champ"""
    title: str
    champ: str
    name: str
    img: str
    desc: str
    tags: str
    stats: str
    url: str

class Champs:
    """Singleton class to dynamically generates a champ upon request"""
    def real_champ(self, name) -> str:
        """Check if a champ is real"""
        _name = name.lower().replace(' ', '')
        for champ in get_champs():
            if champ.lower() == _name:
                return champ
        return None

    def get_champ(self, champ) -> Champ:
        """Dynamically generate the Champ Model object"""
        champ_id = get_champs()[champ]['id']
        title = get_champs()[champ_id]['title']
        img = f"https://ddragon.leagueoflegends.com/cdn/{get_version()}/img/champion/{get_champs()[champ_id]['image']['full']}"
        desc =  get_champs()[champ_id]['blurb']
        tags = ' '.join(get_champs()[champ_id]['tags'])
        stats = f'Health: {get_champs()[champ_id]["stats"]["hp"]} \n \
                Move Speed: {get_champs()[champ_id]["stats"]["movespeed"]} \n \
                Attack Damage: {get_champs()[champ_id]["stats"]["attackdamage"]} \n \
                Attack Range: {get_champs()[champ_id]["stats"]["attackrange"]} \n \
                Attack Speed: {get_champs()[champ_id]["stats"]["attackspeed"]}'
        url = f'https://www.op.gg/champion/{champ_id}/statistics'
        name = get_champs()[champ_id]['name']
        return Champ(
            title=title,
            champ=champ_id,
            name=name,
            img=img,
            desc=desc,
            tags=tags,
            stats=stats,
            url=url
        )
