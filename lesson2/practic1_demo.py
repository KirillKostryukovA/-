import httpx
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


url = "https://quotes.toscrape.com/"

headers = {
    "user-agent": UserAgent().random
}

response = httpx.get(url, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.text, "lxml")

# Теперь парсим 
quotes = soup.find_all("div", class_ = "quote")

# Список, в котором будем сохранять наши цитаты в виде словаря
quotes_list = []
num = 1
for quote in quotes:
    info = {
        "Цитата": quote.find("span", class_ = "text").get_text(),
        "Автор": quote.find("small", class_ = "author").get_text(),
        "Теги": [tag.get_text() for tag in quote.find_all("a", class_ = "tag")]
    }

    quotes_list.append(info)
    num += 1

    if num == 6:
        break

# Выводим наш список с 5-ю цитатами 
if __name__ == "__main__":
    print(quotes_list)