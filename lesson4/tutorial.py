import asyncio

import httpx


async def fetch(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

        return response.text


# Запуск 
url = "https://httpbin.org/get"
result = asyncio.run(fetch(url))
print(result[:200])