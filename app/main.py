import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import create_table
from app.routers import shortener

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Создание таблицы в базе данных при запуске.
    """
    logging.info("Инициализация базы данных...")
    create_table()
    logging.info("База данных инициализирована.")
    yield


app = FastAPI(
    title="Сокращатель URL",
    description="Простое приложение для сокращения URL.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(shortener.router)
