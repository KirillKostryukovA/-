from playwright.sync_api import sync_playwright
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


def scrape_dynamic(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=UserAgent().random
        )
        page = context.new_page()

        page.goto(url, wait_until="networkidle")
        page.wait_for_selector(".quote", timeout=10000)

        soup = BeautifulSoup(page.content(), "lxml")
        quotes = soup.find_all("div", class_ = "quote")

        browser.close()
        return quotes


results = scrape_dynamic("https://quotes.toscrape.com/js/")
print(f"Найдено цитат {len(results)}")