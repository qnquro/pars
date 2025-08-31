# parsers/lenta_parser.py
from bs4 import BeautifulSoup
import logging
from parsers.base_parser import fetch_rss_sync
from DB.categorizer import categorize_article
from DB.manageDB import save_to_database


logger = logging.getLogger(__name__)


# parsers/lenta_parser.py
def parse_lenta_ru_sync():
    """Парсинг Lenta.ru с альтернативными источниками"""
    rss_urls = [
        'https://lenta.ru/rss/news',
        'https://lenta.ru/rss/latest',
        'https://lenta.ru/rss/top7'
    ]

    for url in rss_urls:
        content = fetch_rss_sync(url)
        if content:
            try:
                soup = BeautifulSoup(content, 'xml')
                items = soup.find_all('item')

                news_list = []
                for item in items[:10]:
                    try:
                        title = item.title.text if item.title else 'Без заголовка'
                        link = item.link.text if item.link else '#'
                        description = item.description.text if item.description else 'Нет описания'
                        pub_date = item.pubDate.text if item.pubDate else 'Дата неизвестна'
                        category = categorize_article(title, description)
                        try:
                            description_text = BeautifulSoup(description, 'html.parser').get_text()
                        except:
                            description_text = description

                        news_list ={
                            'short_text': title.strip(),
                            'link': link.strip(),
                            'content': description_text.strip(),
                            'date': pub_date.strip(),
                            'ist': 'Lenta.ru',
                            'category': category
                        }

                        save_to_database(news_list)

                    except Exception as e:
                        continue

                if news_list:
                    return news_list

            except Exception as e:
                continue

    logger.error("Не удалось получить новости Lenta.ru ни из одного источника")
    return []