import logging
import sqlite3

from app.config import settings

DATABASE_FILE = settings.database_file


def get_db():
    """
    Создает зависимость (dependency) для получения сессии базы данных.
    Гарантирует, что соединение с базой данных будет закрыто после использования.
    """
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def create_table():
    """Создает таблицу 'urls', если она не существует."""
    # Используем прямое соединение, так как это разовая операция при старте
    conn = sqlite3.connect(DATABASE_FILE)
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
