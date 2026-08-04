""" Асинхронная вариация парсинга цитаты из сайта """

import asyncio

import httpx
import fake_useragent
from bs4 import BeautifulSoup


# Агент, с помощью которого нас не будет сайт воспринимать как бота, словно человек заходит
user = fake_useragent.UserAgent().random

# Всё необходимое для создания агента
header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "ru-RU,ru;q=0.9",
}

# Ссылка на сайт
url = "https://quotes.toscrape.com/"


# Оборачиваем всю логику асинхронного парсинга в асинхронную функцию 
async def Session():
    async with httpx.AsyncClient() as client:
        # Делаем запрос через Client
        response = await client.get(url)

        # Текст запроса
        html = response.text

        # Парсим HTML
        soup = BeautifulSoup(html, "lxml")

        # Процесс парсинга
        first = soup.find("div", itemtype="http://schema.org/CreativeWork")
        second = first.find_all("span", itemprop = "text")[0].text

        # Выводит фразу, которую я хочу запарсить
        print(second)


# Запуск программы
if __name__ == "__main__":
    asyncio.run(Session())  