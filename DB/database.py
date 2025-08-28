import sqlite3
from datetime import datetime


def create_database():
    conn = sqlite3.connect('easynews.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS EasyNews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT,
        date TEXT,
        ist TEXT,
        link TEXT UNIQUE,
        short_text TEXT,
        content TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    conn.commit()
    conn.close()
    print("База данных создана успешно!")


create_database()