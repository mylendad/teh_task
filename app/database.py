import sqlite3
import logging

from app.config import settings

DATABASE_FILE = settings.database_file


def get_db_connection():
    """Устанавливает соединение с базой данных SQLite."""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    """Создает таблицу 'urls', если она не существует."""
    conn = get_db_connection()
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_url TEXT NOT NULL,
                code TEXT NOT NULL UNIQUE
            )
            """
        )
        conn.commit()
    except sqlite3.Error as e:
        logging.error(f"Ошибка базы данных: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("Инициализация базы данных...")
    create_table()
    logging.info("База данных инициализирована.")
