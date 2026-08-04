import asyncio 

import httpx


async def fetch(client, url):
    response = await client.get(url)
    return response.status_code


async def main():
    urls = [f"https://httpbin.org/get?page={i}" for i in range(1, 11)]

    async with httpx.AsyncClient() as client:
        tasks = [fetch(client, url) for url in urls] 

        results = await asyncio.gather(*tasks)

    print(results)


asyncio.run(main())