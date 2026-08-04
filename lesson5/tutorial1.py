from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto("https://quotes.toscrape.com/js/")
    page.wait_for_selector(".quote")

    html = page.content() # Получаем готовый html после JS
    print(html[:500])

    browser.close()