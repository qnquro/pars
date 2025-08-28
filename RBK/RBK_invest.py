import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
from DB.manageDB import save_to_database
from DB.categorizer import categorize_article


def parse_rbk_invest():
    source_name = "РБК Инвестиции"
    base_url = "https://www.rbc.ru/finances/"
    print("Начало парсинга РБК Инвестиции")

    ua = UserAgent()
    headers = {'user-agent': ua.random}

    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")

        news_items = soup.find_all("div", class_="item")
        print(f"Найдено новостных блоков: {len(news_items)}")

        for news_item in news_items:
            try:
                news_link = news_item.find("a", class_="item__link")
                if not news_link:
                    print("Не найдена ссылка на новость")
                    continue

                card_url = news_link.get("href")
                if not card_url.startswith('http'):
                    card_url = 'https://www.rbc.ru' + card_url

                # Заголовок новости
                title_elem = news_item.find("span", class_="item__title")
                short_text = title_elem.text.strip() if title_elem else ""

                # Дата новости
                date_elem = news_item.find("span", class_="item__category")
                date = date_elem.text.strip() if date_elem else ""

                content = get_article_content(card_url, headers)

                category = categorize_article(short_text, content)

                news_data = {
                    'date': date,
                    'ist': source_name,
                    'link': card_url,
                    'short_text': short_text,
                    'category': category,
                    'content': content
                }

                save_to_database(news_data)
                print(f"Новость сохранена: {short_text}")

                time.sleep(1)

            except Exception as e:
                print(f"Ошибка при обработке новости: {e}")
                continue

    except Exception as e:
        print(f"Ошибка при парсинге РБК Инвестиций: {e}")


# Функция для получения полного текста статьи
def get_article_content(article_url, headers):
    try:
        print(f"Загрузка статьи: {article_url}")
        response = requests.get(article_url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")

        # Пробуем разные селекторы для контента
        content_element = None
        selectors = [
            "div.article__text",
            "div.article__content",
            "div.l-col-center",
            "div[itemprop='articleBody']",
            "div.article-text"
        ]

        for selector in selectors:
            content_element = soup.select_one(selector)
            if content_element:
                break

        if not content_element:
            # Если не нашли по селекторам, попробуем найти любой контентный блок
            content_element = soup.find("div", class_=lambda x: x and "text" in x.lower())

        if content_element:
            # Удаляем ненужные элементы
            for unwanted in content_element.select(
                    ".ad, .banner, .adv, .social, .subscribe, script, style, .inline-item"):
                unwanted.decompose()

            paragraphs = content_element.find_all("p")
            content = " ".join(p.text.replace("\xa0", " ").strip() for p in paragraphs if p.text.strip())
            return content.strip()

        return "Контент не найден"

    except Exception as e:
        print(f"Ошибка при получении контента статьи {article_url}: {e}")
        return ""


if __name__ == "__main__":
    parse_rbk_invest()