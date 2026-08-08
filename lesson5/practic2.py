""" Исправленная версия practic'а 1-го, теперь парсинг происходит параллельно! """

import asyncio
import json
import time

from playwright.async_api import async_playwright
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


# Максимум выполняется 6 запросов
semaphore = asyncio.Semaphore(6)

# Парсим одну страницу
async def catch_one_page(html, page_num):
    soup = BeautifulSoup(html, "lxml")
    quotes = soup.find_all("div", class_ = "quote")

    quotes_list = []
    for quote in quotes:
        info = {
            "Цитата": quote.find("span", class_ = "text").get_text(),
            "Автор": quote.find("small", class_ = "author").get_text(),
            "Ссылка на автора": "https://quotes.toscrape.com" + quote.find("a")["href"],
            "Теги": [tag.get_text() for tag in quote.find_all("a", class_ = "tag")],
        }

        quotes_list.append(info)

    print(f"Обработана страница:{page_num}, собрано {len(quotes_list)} цитат...")
    return quotes_list


# Собираем ссылки на следующие страницы
async def fetch_pages(url):
    # Список задач для параллельного выполнения
    tasks_list = []

    async with async_playwright() as p:
        page_num = 1

        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent=UserAgent().random
        )

        page = await context.new_page()
        await page.goto(url, wait_until="networkidle")

        await page.wait_for_selector("div.quote", timeout=2000)

        try:
            while True:
                print(f"Обрабатываем страницу {page_num}")
                html = await page.content()

                task = asyncio.create_task(catch_one_page(html, page_num))
                tasks_list.append(task)

                page_num += 1

                # Скролл вниз 
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

                next_button = page.locator("li.next > a")

                if await next_button.is_visible():
                    await next_button.click()
                    await page.wait_for_load_state("networkidle")
                else:
                    print("Парсинг окончен!")
                    break

        except asyncio.TimeoutError as e:
            print(f"Ошибка! Долгий парсинг: {e}")
        except Exception as e:
            print(f"Произошла ошибка: {e}!")
        finally:
            await browser.close()

    # Запускаем обработку всех выполненных страниц
    results = await asyncio.gather(*tasks_list)

    # Распаковываем результаты всех страниц в один общий список
    all_quotes = []
    for result in results:
        all_quotes.extend(result)

    return all_quotes


# Главная функция, через которую происходит запуск парсинга
async def main():
    # Время начала парсинга 
    start_time = time.time()

    result = await fetch_pages("https://quotes.toscrape.com/")

    # Записываем наши цитаты в JSON-файл
    with open("practic2.json", "w", encoding="utf-8") as file:
        json.dump(result, file, ensure_ascii=False, indent=4)

    # Время окончания парсинга
    end_time = time.time()

    print(f"Парсинг окончен! Время выполнения парсинга: {end_time-start_time} секунд!")
    return result


# Запуск парсинга
if __name__ == "__main__":
    asyncio.run(main())