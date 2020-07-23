from selenium import webdriver
import json
import random
from time import sleep
from selenium.webdriver.common.keys import Keys

class Screenshot:
    def __init__(self, driver, name, prefix=None):
        self.driver = driver
        self.name = name
        if prefix is None:
            self.url = f'https://www.op.gg/champion/{self.name}/statistics'
        else:
            self.url = f'https://{prefix}.op.gg/summoner/userName={self.name}'

    def runes(self):
        self.driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
        self.driver.get(self.url)
        self.driver.set_window_size(733,481)
        seed = str(random.randint(0,99999))
        self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div[5]/div[1]/div/div[1]/div/table/tbody[2]').screenshot(f'../temp/{seed}.png')
        self.driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'w')
        return seed

    def build(self):
        self.driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
        self.driver.get(self.url)
        self.driver.set_window_size(733,680)
        seed = str(random.randint(0,99999))
        self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div[5]/div[1]/div/div[1]/table[2]').screenshot(f'../temp/{seed}.png')
        self.driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'w')
        return seed

    def skills(self):
        self.driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
        self.driver.get(self.url)
        self.driver.set_window_size(734,150)
        seed = str(random.randint(0,99999))
        self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div[5]/div[1]/div/div[1]/table[1]/tbody[2]').screenshot(f'../temp/{seed}.png')
        self.driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'w')
        return seed

    def champ_stats(self):
        self.driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
        self.driver.get(self.url)
        self.driver.set_window_size(334,692)
        seed = str(random.randint(0,99999))
        self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div[5]/div[1]/div/div[2]/div[1]/div[2]').screenshot(f'../temp/{seed}.png')
        self.driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'w')
        return seed
        
    def sums(self):
        self.driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
        self.driver.get(self.url)
        self.driver.set_window_size(750,135)
        seed = str(random.randint(0,99999))
        self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div[5]/div[1]/div/div[1]/table[1]/tbody[1]').screenshot(f'../temp/{seed}.png')
        self.driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'w')
        return seed

    def matchups(self):
        self.driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
        self.driver.get(self.url)
        self.driver.set_window_size(342,620)
        self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div[1]/div/ul/li[6]/a').click()
        seed = str(random.randint(0,99999))
        sleep(.5)
        self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div[5]/div[7]/div/div[2]/div[3]').screenshot(f'../temp/{seed}.png')
        self.driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'w')
        return seed

    def get_match_info(self):
        self.driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
        self.driver.get(self.url)
        seed = str(random.randint(0,99999))
        self.driver.find_element_by_xpath('//*[@id="GameAverageStatsBox-summary"]/div[1]').screenshot(f'../temp/{seed}.png')
        self.driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'w')
        return seed

    def get_matches(self):
        self.driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
        self.driver.get(self.url)
        seed = str(random.randint(0,99999))
        self.driver.set_window_size(1080,1920) # May need manual adjustment
        self.driver.find_element_by_xpath('//*[@id="SummonerLayoutContent"]/div[2]/div[2]/div').screenshot(f'../temp/{seed}.png')
        self.driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'w')
        return seed