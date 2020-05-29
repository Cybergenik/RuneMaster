from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import random
import os
import json
from riotwatcher import LolWatcher, ApiError

RIOT_API_KEY = os.getenv("RIOT_API_KEY")
lol_watcher = LolWatcher(RIOT_API_KEY)

class Summon:
    def __init__(self, region="na1", name="jareco", ss=False):
        try:
            player_info = lol_watcher.summoner.by_name(region, name)
            player_stats = lol_watcher.league.by_summoner(region, player_info['id'])
            self.real_player = True
        except:
            self.real_player = False
        if self.real_player:
            self.player_name = player_info['name']
            self.player_icon = player_info['profileIconId']
            self.player_level = player_info['summonerLevel']
            self.player_rank_img = f'./images/{player_stats[0]["tier"].lower()}.png'
            self.player_rank = f'{player_stats[0]["tier"].lower().capitalize()} {player_stats[0]["rank"]}'
            self.player_win = f'{round((player_stats[0]["wins"] / (player_stats[0]["wins"] + player_stats[0]["losses"])) * 100)}%'
            
            with open('regions.json') as f:
                regions = json.load(f)
            for prefix in regions:
                if regions[prefix] == region.lower(): 
                    self.url = 'https://'+prefix+'.op.gg/summoner/userName='+self.player_name
                    break
            if ss == True:
                if os.name == "nt":
                    options = webdriver.FirefoxOptions()
                    options.add_argument('--headless')
                    options.add_argument('--no-sandbox')
                    options.add_argument('--disable-dev-shm-usage')
                    self.driver = webdriver.Firefox(executable_path="./geckodriver.exe",options=options)
                elif os.name == "posix":
                    options = webdriver.ChromeOptions()
                    options.binary_location = os.getenv("GOOGLE_CHROME_BIN")
                    options.add_argument('--hide-scrollbars')
                    options.add_argument('--headless')
                    options.add_argument('--disable-dev-shm-usage')
                    options.add_argument('--no-sandbox')
                    self.driver = webdriver.Chrome(executable_path=os.getenv("CHROMEDRIVER_PATH"), chrome_options=options)
                else:
                    raise Exception('Unknown Operating System, please use either a UNIX based OS or Windows')
                self.driver.get(self.url)

    def get_real_player(self):
        return self.real_player

    def get_name(self):
        return self.player_name
    
    def get_url(self):
        return self.url
        
    def get_icon(self):
        return self.player_icon
    
    def get_level(self):
        return self.player_level
    
    def get_rank_img(self):
        return self.player_rank_img

    def get_rank(self):
        return self.player_rank

    def get_win(self):
        return self.player_win

    def get_match_info(self):
        seed = str(random.randint(0,99999))
        self.driver.find_element_by_xpath('//*[@id="GameAverageStatsBox-summary"]/div[1]').screenshot('./images/vape'+seed+'.png')
        return seed

    def get_matches(self):
        self.driver.set_window_size(800,1800) # May need manual adjustment
        seed = str(random.randint(0,99999))
        self.driver.find_element_by_xpath('//*[@id="SummonerLayoutContent"]/div[2]/div[2]/div').screenshot('./images/vape'+seed+'.png')
        return seed

    def kill_seed(self, seed):
        '''
        Deletes temporary png files.
        '''
        if os.path.exists("./images/vape"+seed+".png"):
           os.remove("./images/vape"+seed+".png")
        else:
           print(seed+".png does not exist")
    
    def kill_driver(self):
        self.driver.quit()
