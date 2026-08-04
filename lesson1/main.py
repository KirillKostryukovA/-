import requests
import fake_useragent
from bs4 import BeautifulSoup


user = fake_useragent.UserAgent().random

header = {"user-agent": user}

link = "https://browser-info.ru/"

response = requests.get(link, headers=header).text
soup = BeautifulSoup(response, "lxml")

# Javascript status
# block = soup.find("div", id = "tool_padding")
# js = block.find("div", id = "javascript_check")
# result_js = js.find_all("span")[1].text

# print(result_js)


# User agent
# brawser = soup.find("div", id="tool_padding")
# stmt = brawser.find("div", id="user_agent").text

# print(stmt)


# # Окошко размеры  
# window_1 = soup.find("div", id = "window_size").text

# print(window_1)

