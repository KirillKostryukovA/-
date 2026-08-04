from playwright.sync_api import sync_playwright
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


def fetch_page(url):
    with sync_playwright() as p:
        # Бот открывает браузер (headless=True - не показывает сам браузер бота)
        browser = p.chromium.launch(headless=False)

        # Бот маскируется под обычного человека, зашедшего с устройства на сайт
        context = browser.new_context(
            user_agent=UserAgent().random
        )

        # Бот открывает новую страничку (нажимает на +)
        page = context.new_page()

        # Бот вбивает нашу ссылку и переходит по ней
        page.goto(url, wait_until="networkidle")

        # Бот ищет элемент и ждёт 10 секунд до полной прогрузки сайта
        page.wait_for_selector("div.row", timeout=10000)

        # Готовый html-файл
        html = page.content()

        # Начало парсинга
        soup = BeautifulSoup(html, "lxml")
        books = soup.find_all("article", class_ = "product_pod")

        # Скролл вниз до конца страницы
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

        # Ищет любой кликабельный элемент с текстом "Next" 
        page.get_by_text("next").click()
        page.wait_for_timeout(2000) # Ждём 2 секунды

        # Вписать в строку поиска "python" и нажать на кнопку Enter
        page.fill("input#search", "python")
        page.press("input#search", "Enter")

        browser.close()
        # return books


fetch_page("https://books.toscrape.com/")
# books_list = fetch_page("https://books.toscrape.com/")
# print(f"Найдено книг: {len(books_list)}")