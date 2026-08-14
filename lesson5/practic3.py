import asyncio

from playwright.async_api import async_playwright
from fake_useragent import UserAgent


async def fetch_page(page):
    await page.wait_for_selector("article", state="visible")
    await asyncio.sleep(2)
    
    # Берём родительский <p> и сразу получаем весь текст "+15°"
    temp_container = page.locator("p[class*='AppFactTemperature_content']").first
    temp_text = await temp_container.inner_text()
    
    return {"now": temp_text.strip()}


async def main():
    current_url = "https://yandex.ru/pogoda/ru/liski"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(user_agent=UserAgent().random)
        page = await context.new_page()
        
        await page.goto(current_url, wait_until="load")

        result = await fetch_page(page)
        print(result)
        
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())