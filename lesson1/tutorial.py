import httpx
from bs4 import BeautifulSoup


link = "https://toolbox.googleapps.com/apps/browserinfo/?lang=ru"
response = httpx.get(link).text

bs = BeautifulSoup(response, "lxml")


with open("templates/index.html") as file:
    # Вытаскиваем значение IP-адреса 
    first = file.read()

    