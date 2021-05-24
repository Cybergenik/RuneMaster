from io import BytesIO
from playwright.async_api import async_playwright

async def startup():
    playwright = await async_playwright().start()
    print('Starting web drive for the first time...')
    browser = await playwright.chromium.launch()
    print("Launched browser")
    while True:
        yield await browser.new_page()

PW = startup()

async def get_screenshot(name:str, action:str, prefix=None) -> BytesIO:
    try:
        page = await PW.__anext__()
    except Exception as e:
        print(f'Unable to get new page: \n {e}')
    print("Got page")
    if prefix is None:
        url = f'https://www.op.gg/champion/{name}/statistics'
    else:
        if prefix == "kr": prefix = "www"
        url = f'https://{prefix}.op.gg/summoner/userName={name}'
    try:
        await page.goto(url)
        if action == "runes":
            await page.set_viewport_size({"width": 734, "height": 607})
            await page.click("body > div.l-wrap.l-wrap--champion > div.l-container > div > div.tabWrap._recognized > div.l-champion-statistics-content.tabItems > div.tabItem.Content.championLayout-overview > div > div.l-champion-statistics-content__main > div > table")
        elif action == "build":
            await page.set_viewport_size({"width": 734, "height": 667})
            await page.click("body > div.l-wrap.l-wrap--champion > div.l-container > div > div.tabWrap._recognized > div.l-champion-statistics-content.tabItems > div.tabItem.Content.championLayout-overview > div > div.l-champion-statistics-content__main > table:nth-child(2)")
        elif action == "skills":
            await page.set_viewport_size({"width": 734, "height": 340})
            await page.click("body > div.l-wrap.l-wrap--champion > div.l-container > div > div.tabWrap._recognized > div.l-champion-statistics-content.tabItems > div.tabItem.Content.championLayout-overview > div > div.l-champion-statistics-content__main > table.champion-overview__table.champion-overview__table--summonerspell")
        elif action == "stats":
            await page.set_viewport_size({"width": 1200, "height": 265})
            await page.click("body > div.l-wrap.l-wrap--champion > div.l-container > div > div.l-champion-statistics-header")
        elif action == "matches":
            await page.set_viewport_size({"width": 690, "height": 1250})
            await page.click("#SummonerLayoutContent > div.tabItem.Content.SummonerLayoutContent.summonerLayout-summary > div.RealContent > div > div.Content")
        elif action == "soloranked_matches":
            await page.click("#right_gametype_soloranked > a")
            await page.set_viewport_size({"width": 690, "height": 1250})
            await page.click("#SummonerLayoutContent > div.tabItem.Content.SummonerLayoutContent.summonerLayout-summary > div.RealContent > div > div.Content")
        elif action == "flexranked_matches":
            await page.click("#right_gametype_flexranked > a")
            await page.set_viewport_size({"width": 690, "height": 1250})
            await page.click("#SummonerLayoutContent > div.tabItem.Content.SummonerLayoutContent.summonerLayout-summary > div.RealContent > div > div.Content")
        elif action == "leaderboard":
            await page.click("body > div.l-wrap.l-wrap--summoner > div.l-menu > ul > li:nth-child(6) > a")
            await page.set_viewport_size({"width": 970, "height": 391})
            await page.click("body > div.l-wrap.l-wrap--ranking > div.l-container > div.LadderRankingLayoutWrap > div > div > div > div.ranking-highest")
        else:
            return None
        print("got element")
    except Exception as e:
        print(f'Error in Screenshot at: {url} :\n {e}')

    screenshot_bytes = BytesIO(await page.screenshot())
    await page.close()
    screenshot_bytes.seek(0)
    return screenshot_bytes
