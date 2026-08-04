""" Доработанная и улучшенная версия practic 3 """

""" То, что мы делали в practic2, теперь нужно сначала записать в словарь (первые 5 цитат), затем записать в JSON """
import json

import httpx
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


url = "https://quotes.toscrape.com/"

# Заголовки, необходимые для того, чтобы наша программа могла парсить сайт под видом устройства пользователя
headers = {
    "user-agent": UserAgent().random
}

response = httpx.get(url, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.text, "lxml")

# Теперь парсим первые 5 цитат
quotes = soup.find_all("div", class_ = "quote")[:5]

# Список, в котором будем сохранять наши цитаты в виде словаря
quotes_list = []

for quote in quotes:
    info = {
        "Цитата": quote.find("span", class_ = "text").get_text(),
        "Автор": quote.find("small", class_ = "author").get_text(),
        "Ссылка на автора": "https://quotes.toscrape.com" + quote.find("a")["href"],
        "Теги": [tag.get_text() for tag in quote.find_all("a", class_ = "tag")],
    }

    quotes_list.append(info)


# Записываем наш список с цитатами в виде JSON
with open("quotes.json", "w", encoding="utf-8") as file:
    json.dump(quotes_list, file, ensure_ascii=False, indent=4)


# Выводим наш список с 5-ю цитатами 
if __name__ == "__main__":
    pretty_json = json.dumps(quotes_list, ensure_ascii=False, indent=4)
    print(pretty_json)