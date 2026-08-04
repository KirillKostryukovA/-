from playwright.sync_api import sync_playwright
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


def fetch_page(url):
    with sync_playwright() as p:
        # Бот открывает браузер (headless=True - не показывает сам браузер бота)
        browser = p.chromium.launch(headless=True)

        # Бот маскируется под обычного человека, зашедшего с устройства на сайт
        context = browser.new_context(
            user_agent=UserAgent().random
        )

        # Бот открывает новую страничку (нажимает на +)
        page = context.new_page()

        # Бот вбивает нашу ссылку и переходит по ней
        page.goto(url, wait_until="networkidle")

        # Бот ищет элемент и ждёт 10 секунд до полной прогрузки сайта
        page.wait_for_event("div", class_ = "row", timeout=10000)

        