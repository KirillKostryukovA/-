import asyncio

import httpx
from bs4 import BeautifulSoup


# Максимумм 5 одновременных запросов 
semaphore = asyncio.Semaphore(5)


async def fetch_quote(client, page):
    async with semaphore:
        url = f"https://quotes.toscrape.com/page/{page}/"
        response = await client.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "lxml")
            quotes = soup.find_all("div", class_="quote")
            return len(quotes)

        return 0


async def main():
    async with httpx.AsyncClient() as client:
        tasks = [fetch_quote(client, p) for p in range(1, 11)]
        results = await asyncio.gather(*tasks)

    print(f"Всего страниц с цитатами {sum(1 for r in results if r > 0 )}")


asyncio.run(main())