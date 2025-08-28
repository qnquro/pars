#RBK_NEWS.py

from DB.manageDB import save_to_database

import requests
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent
import time
#----

all_url = []

#----

#----



ist ="РБК Новости"
url = "https://www.rbc.ru/short_news"
link = "https://www.rbc.ru/short_news"
# импортировал fake_useragent, но не использовал его. зачем?
ua = UserAgent()
headers = {'user-agent': ua.random}

response = requests.get(url, headers=headers)

soup = BS(response.text, "lxml")

data = soup.find_all("div", class_="js-news-feed-item js-yandex-counter")



for el in data:
	time.sleep(1)
#использовать глобальную переменную - плохой тон
	global content
	card_url = el.find("a", class_="item__link rm-cm-item-link js-rm-central-column-item-link").get("href")
	all_url.append(card_url)


	for card_url in all_url:
		try:
			response = requests.get(card_url, headers=headers)

			soup = BS(response.text, "lxml")

			data = soup.find("div", class_="article__text article__text_free")

			content = data.find("p").text.replace("\xa0", "")
		except AttributeError:
			print("AttributeError")
			content = ""
		

	short_text = el.find("a", class_="item__link rm-cm-item-link js-rm-central-column-item-link").text.replace("\n", "")

	category = el.find("a", class_="item__category").text.replace(",\xa0", "")

	date = el.find("span", class_="item__category").text

	all_info = {'date': date, 'ist': ist, 'link': card_url, 'short_text': short_text, 'category': category, 'content': content}

    save_to_database(all_info)
	
