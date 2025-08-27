import sqlite3
from datetime import datetime
import re

def normalize_date(date_str):
    if not date_str:
        return None
    date_str = str(date_str).lower().strip()

    try:
        if re.match(r'\d{2}:\d{2}:\d{4}', date_str):
            return date_str
        date_formats = [
            '%Y-%m-%d', '%d.%m.%Y', '%d/%m/%Y', '%d-%m-%Y',
            '%Y.%m.%d', '%Y/%m/%d', '%d %b %Y', '%d %B %Y'
        ]

        for fmt in date_formats:
            try:
                dt = datetime.strptime(date_str, fmt)
                return dt.strftime('%d:%m:%Y')
            except ValueError:
                continue
        if ' ' in date_str:
            date_part = date_str.split(' ')[0]
            for fmt in date_formats:
                try:
                    dt = datetime.strptime(date_part, fmt)
                    return dt.strftime('%d:%m:%Y')
                except ValueError:
                    continue

    except Exception as e:
        print(f"Ошибка при преобразовании даты '{date_str}': {e}")
    return date_str


def save_to_database(news_item):
    category = news_item.get('category', '').lower().strip()
    date = normalize_date(news_item.get('date'))
    ist = news_item.get('ist', '').strip()
    link = news_item.get('link', '').strip()
    short_text = news_item.get('short_text', '').strip()
    content = news_item.get('content', '').strip()

    if not all([category, ist, link, short_text]):
        print("Отсутствуют обязательные поля")
        return False

    try:
        conn = sqlite3.connect('news.db')
        cursor = conn.cursor()

        #проверка на уже существующую новость
        cursor.execute('SELECT id FROM News WHERE link = ?', (link,))
        if cursor.fetchone():
            print(f"Новость уже существует: {link}")
            return False

        cursor.execute('''
        INSERT INTO News (category, date, ist, link, short_text, content)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (category, date, ist, link, short_text, content))

        conn.commit()
        conn.close()

        print(f"Новость сохранена: {short_text}")
        return True

    except sqlite3.Error as e:
        print(f"Ошибка при сохранении в базу данных: {e}")
        return False