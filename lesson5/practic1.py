""" Парсим сайт цитат с помощью playwright + bs4 """
""" Тут всё равно последовательный парсинг, исправлено в pracric2.py """

import asyncio
import time
import random

from playwright.async_api import async_playwright
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


# Максимум 6 одновременных парсеров
semaphore = asyncio.Semaphore(6)

quotes_list = []


# Асинхронной функция для поиска цитат из страниц
async def fetch_pages(url):
    async with async_playwright() as p:
        page_num = 1

        browser = await p.chromium.launch(headless=False)

        # Бот маскируется под обычного пользователя 
        context = await browser.new_context(
            user_agent=UserAgent().random
        )

        page = await context.new_page()
        await page.goto(url, wait_until="networkidle")

        await page.wait_for_selector("div.quote", timeout=3000)

        try:
            # Начало парсинга каждой странички
            while url:
                print(f"Парсинг страницы: {page_num}")
                page_num += 1

                # Готовый html-файл для парсинга страницы
                html = await page.content()

                soup = BeautifulSoup(html, "lxml")
                quotes = soup.find_all("div", class_ = "quote")

                for quote in quotes:
                    info = {
                        "Цитата": quote.find("span", class_ = "text").get_text(),
                        "Автор": quote.find("small", class_ = "author").get_text(),
                        "Ссылка на автора": "https://quotes.toscrape.com" + quote.find("a")["href"],
                        "Теги": [tag.get_text() for tag in quote.find_all("a", class_ = "tag")],
                    }

                    quotes_list.append(info)

                # Скролл 0 по оси x и до конца по оси y
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

                # Ищет любой кликабельный элемент с текстом "next"
                next_button = page.locator("li.next > a")

                if next_button is None:
                    print("Парсинг окончен!")
                    break
                else:
                    await next_button.click()
                    await page.wait_for_load_state("networkidle")

            return quotes_list
        
        except Exception as e:
            print(f"Произошла ошибка:: {e}")
        finally:
            await browser.close()


# Главная асинхронная функция, в которой происходит параллельный парсинг
async def main():
    time_start = time.time()
    current_url = "https://quotes.toscrape.com/"

    result = await fetch_pages(current_url)
    asyncio.gather(*result)

    time_end = time.time()

    print(f"Всего было запарсено {len(quotes_list)} цитат!")
    print(f"Всего было затрачено времени на парсинг: {time_end - time_start} секунд!")


# Запуск нашего парсера
asyncio.run(main())