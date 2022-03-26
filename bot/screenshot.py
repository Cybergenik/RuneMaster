from io import BytesIO
from typing import Coroutine, Any
from copy import copy
from playwright.async_api import async_playwright, Page
from cachetools import TTLCache
from datetime import datetime, timedelta

class Browser:
    """Singleton class to represent Playwright Browser for screenshots"""
    def __init__(self):
        self.__pw = None
        self.__cache = TTLCache(maxsize=500, ttl=timedelta(hours=6), timer=datetime.now)
    
    async def __new_page(self) -> Coroutine[Any, Any, Page]:
        """Creates and returns new page, caller assumes ownership and must close page"""
        try:
            if not self.__pw:
                self.__pw = await async_playwright().start()
                self.__browser = await self.__pw.chromium.launch()
            return await self.__browser.new_page()
        except Exception as e:
            print(f'Unable to get new page: \n {e}')

    async def get_cached_screenshot(self, name:str, action:str) -> BytesIO:
        key = f'{action}-{name}'
        if key in self.__cache:
            return copy(self.__cache[key])
        else:
            img = await self.__cached_screenshot(name, action)
            self.__cache[key] = copy(img)
        return img

    async def __cached_screenshot(self, name:str, action:str) -> BytesIO:
        """Cached screenshot generator, use only for immutable (mostly) data"""
        url = f'https://www.op.gg/champion/{name}/statistics'
        page = await self.__new_page()
        try:
            await page.goto(url)
            if action == "runes":
                await page.set_viewport_size({"width": 734, "height": 607})
                await page.click("//html/body/div[1]/div[5]/div[1]/table[3]")
            elif action == "build":
                await page.set_viewport_size({"width": 734, "height": 667})
                await page.click("//html/body/div[1]/div[5]/div[1]/table[2]")
            elif action == "skills":
                await page.set_viewport_size({"width": 734, "height": 340})
                await page.click("//html/body/div[1]/div[5]/div[1]/table[1]")
            elif action == "stats":
                await page.set_viewport_size({"width": 1200, "height": 265})
                await page.click("//html/body/div[1]/div[1]/div[1]")
            else:
                return None
            await page.mouse.move(0, 0)
        except Exception as e:
            print(f'Error in Cached Screenshot at: {url} :\n {e}')
            await page.close()
            return None
        screenshot_bytes = BytesIO(await page.screenshot())
        await page.close()
        screenshot_bytes.seek(0)
        return screenshot_bytes

    async def get_screenshot(self, name:str, action:str, prefix: str) -> BytesIO:
        """Screenshot generator, use when data is ephemeral"""
        if prefix == "kr": prefix = "www"
        url = f'https://{prefix}.op.gg/summoner/userName={name}'
        page = await self.__new_page()
        try:
            await page.goto(url)
            if action == "matches":
                await page.set_viewport_size({"width": 690, "height": 1250})
                await page.click("//html/body/div[1]/div[5]/div[2]")
            elif action == "soloranked_matches":
                await page.click("//html/body/div[1]/div[5]/div[2]/div[1]/ul/li[2]/button")
                await page.wait_for_selector("//html/body/div[1]/div[5]/div[2]/ul")
                await page.set_viewport_size({"width": 690, "height": 1250})
                await page.click("//html/body/div[1]/div[5]/div[2]")
            elif action == "flexranked_matches":
                await page.click("//html/body/div[1]/div[5]/div[2]/div[1]/ul/li[3]/button")
                await page.wait_for_selector("//html/body/div[1]/div[5]/div[2]/ul")
                await page.set_viewport_size({"width": 690, "height": 1250})
                await page.click("//html/body/div[1]/div[5]/div[2]")
            elif action == "leaderboard":
                #await page.click("body > div.l-wrap.l-wrap--summoner > div.l-menu > ul > li:nth-child(6) > a")
                await page.set_viewport_size({"width": 970, "height": 391})
                await page.click("//html/body/div[1]/div[5]/div[2]")
            else:
                return None
            await page.mouse.move(0, 0)
        except Exception as e:
            print(f'Error in Screenshot at: {url} :\n {e}')
            await page.close()
            return None
        screenshot_bytes = BytesIO(await page.screenshot())
        await page.close()
        screenshot_bytes.seek(0)
        return screenshot_bytes

