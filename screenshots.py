from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import random
import json
import requests

class Screenshots:
    def __init__(self, champ):
        response = requests.get('https://ddragon.leagueoflegends.com/cdn/10.10.3216176/data/en_US/champion.json')
        self.real = False
        for name in response.json()['data']:
            if champ == name.lower():
                self.champ = response.json()['data'][name]['name']
                URL = 'https://champion.gg/champion/'+self.champ
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
                self.real = True
                break

    def get_real(self) -> bool:
        return self.real 
    def runes(self):
        S = lambda X: self.driver.execute_script('return document.querySelector("#perks-app > div").scroll'+X)
        self.driver.set_window_size(S('Width'),S('Height')) # May need manual adjustment        
        seed = str(random.randint(0,99999))
        self.driver.find_element_by_xpath('//*[@id="perks-app"]/div').screenshot('./images/vape'+seed+'.png')
        self.driver.close()
        return seed

    def build(self):
        seed = str(random.randint(0,99999))
        self.driver.find_element_by_xpath('/html/body/div/div[2]/div[3]/div[2]/div[2]/div/div/div[2]/div[1]/div[1]').screenshot('./images/vape'+seed+'.png')
        self.driver.close()
        return seed

    def skills(self):
        seed = str(random.randint(0,99999))
        self.driver.find_element_by_xpath('/html/body/div/div[2]/div[3]/div[2]/div[2]/div/div/div[1]/div[1]').screenshot('./images/vape'+seed+'.png')
        self.driver.close()
        return seed

    def stats(self):
        S = lambda X: self.driver.execute_script('return document.querySelector("body > div > div.main-container > div.page-content > div.ng-scope > div.champion-area.ng-scope > div > div > div.col-xs-12.col-sm-9.col-md-4.champion-statistics").scroll'+X)
        self.driver.set_window_size(S('Width')+200,S('Height')+200)
        seed = str(random.randint(0,99999))
        self.driver.find_element_by_xpath('/html/body/div/div[2]/div[3]/div[2]/div[1]/div/div/div[2]').screenshot('./images/vape'+seed+'.png')
        self.driver.close()
        return seed
        
    def sums(self):
        seed = str(random.randint(0,99999))
        self.driver.find_element_by_xpath('/html/body/div/div[2]/div[3]/div[2]/div[1]/div/div/div[4]/div[7]').screenshot('./images/vape'+seed+'.png')
        self.driver.close()
        return seed

    def matchups(self):
        S = lambda X: self.driver.execute_script('return document.querySelector("body > div > div.main-container > div.page-content > div.ng-scope > div.matchups > div > div.row.counter-row").scroll'+X)
        self.driver.set_window_size(S('Width')+200,S('Height')+200)
        seed = str(random.randint(0,99999))
        self.driver.find_element_by_xpath('/html/body/div/div[2]/div[3]/div[2]/div[3]/div/div[2]').screenshot('./images/vape'+seed+'.png')
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
