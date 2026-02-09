import logging

from fastapi import FastAPI

from app.database import create_table
from app.routers import shortener

app = FastAPI(
    title="Сокращатель URL",
    description="Простое приложение для сокращения URL.",
    version="0.1.0",
)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


@app.on_event("startup")
def on_startup():
    """
    Создание таблицы в базе данных при запуске.
    """
    logging.info("Инициализация базы данных...")
    create_table()
    logging.info("База данных инициализирована.")


app.include_router(shortener.router)
