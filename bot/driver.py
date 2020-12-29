import os
from functools import lru_cache
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class _Driver:
    def __init__(self):
        print('Starting web drive for the first time...')
        self.options = webdriver.ChromeOptions()
        self.options.binary_location = os.getenv("GOOGLE_CHROME_BIN")
        self.options.add_argument('--headless')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(executable_path=os.getenv("CHROMEDRIVER_PATH"), options=self.options)
    def reset(self):
        print('restarting driver...')
        self.driver.quit()
        self.driver = webdriver.Chrome(executable_path=os.getenv("CHROMEDRIVER_PATH"), options=self.options)

@lru_cache(maxsize=1)
def get_driver() -> _Driver:
    return _Driver()