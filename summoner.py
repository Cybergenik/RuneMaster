from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import random
import os
from riotwatcher import LolWatcher, ApiError

RIOT_API_KEY = os.getenv("RIOT_API_KEY")
lol_watcher = LolWatcher(RIOT_API_KEY)
my_region = 'NA1'

class Summon:
    def __init__(self, name):
        try:
            self.player_info = lol_watcher.summoner.by_name(my_region, name)
            self.player_stats = lol_watcher.league.by_summoner(my_region, self.player_info['id'])
            self.real_player = True
        except:
            self.real_player = False
        if self.real_player:
            URL = 'https://na.op.gg/summoner/userName='+self.name
            if os.name == "nt":
                options = webdriver.FirefoxOptions()
                options.add_argument('--headless')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                self.driver = webdriver.Firefox(executable_path="./geckodriver.exe",options=options)
            elif os.name == "posix":
                options = webdriver.ChromeOptions()
                options.binary_location = os.getenv("GOOGLE_CHROME_BIN")
                options.add_argument('--headless')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--no-sandbox')
                self.driver = webdriver.Chrome(executable_path=os.getenv("CHROMEDRIVER_PATH"), chrome_options=options)
            else:
                raise Exception('Unknown Operating System, please use either a UNIX based OS or Windows')
            self.driver.get(URL)

    def get_real_player(self):
        return self.real_player

    def get_player_info(self):
        return self.player_info
        
    def get_player_stats(self):
        return self.player_stats
        
    def get_ranked_info(self):
        seed = str(random.randint(0,99999))
        self.driver.find_element_by_xpath('//*[@id="GameAverageStatsBox-matches"]').screenshot('./images/vape'+seed+'.png')
        self.driver.close()
        return seed

    def get_matches(self):
        seed = str(random.randint(0,99999))
        self.driver.find_element_by_xpath('//*[@id="SummonerLayoutContent"]/div[2]/div[2]/div/div[2]/div[3]').screenshot('./images/vape'+seed+'.png')
        self.driver.close()
        return seed

    def kill_seed(self, seed):
        '''
        Deletes temporary png files.
        '''
        if os.path.exists("./images/vape"+seed+".png"):
           os.remove("./images/vape"+seed+".png")
        else:
           print(seed+".png does not exist")
