import sqlite3
from datetime import datetime


def create_database():
    conn = sqlite3.connect('easynews.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS EasyNews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT NOT NULL,
        title TEXT NOT NULL,
        content TEXT,
        date TEXT,
        category TEXT
    )
    ''')

    conn.commit()
    conn.close()
    print("База данных создана успешно!")


create_database()