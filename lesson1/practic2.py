# Парсинг цитат с quotes.toscrape.com
import httpx 
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


url = "https://quotes.toscrape.com/"
headers = {"user-agent": UserAgent().random}

response = httpx.get(url, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.text, "lxml")

# Находим все цитаты
quotes = soup.find_all("div", class_ ="quote")

for quote in quotes:
    text = quote.find("span", class_ = "text").get_text()
    author = quote.find("small", class_ = "author").get_text()
    tags = [tag.get_text() for tag in quote.find_all("div", class_ = "tags")]

    print(f"Цитата: {text}")
    print(f"Автор: {author}")
    print(f"Теги: {', '.join(tags)}")
    print("-" * 50)