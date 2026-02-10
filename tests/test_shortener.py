import os

import pytest
from app.database import create_table
from app.main import app
from httpx import ASGITransport, AsyncClient

DATABASE_FILE = "test_shortener.db"


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Настройка тестовой базы данных."""
    # Переопределяем файл базы данных
    import app.database

    app.database.DATABASE_FILE = DATABASE_FILE
    create_table()
    yield
    os.remove(DATABASE_FILE)


@pytest.mark.asyncio
async def test_create_short_url():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post(
            "/shorten", json={"original_url": "https://example.com"}
        )
    assert response.status_code == 200
    data = response.json()
    assert "code" in data
    assert data["original_url"] == "https://example.com/"


@pytest.mark.asyncio
async def test_redirect_to_original_url():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        # Сначала создаем короткий URL
        response = await ac.post(
            "/shorten", json={"original_url": "https://example.com/test-redirect"}
        )
        assert response.status_code == 200
        code = response.json()["code"]

        # Теперь тестируем перенаправление
        redirect_response = await ac.get(f"/{code}", follow_redirects=False)
        assert redirect_response.status_code == 307
        assert (
            redirect_response.headers["location"] == "https://example.com/test-redirect"
        )


@pytest.mark.asyncio
async def test_short_url_not_found():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/nonexistentcode")
    assert response.status_code == 404
    assert response.json() == {"detail": "Короткий URL не найден"}


@pytest.mark.asyncio
async def test_invalid_url():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post("/shorten", json={"original_url": "not-a-url"})
    assert response.status_code == 422  # Ошибка валидации Pydantic


@pytest.mark.asyncio
async def test_update_short_url():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        # Сначала создаем короткий URL
        response = await ac.post(
            "/shorten", json={"original_url": "https://example.com/to-be-updated"}
        )
        assert response.status_code == 200
        code = response.json()["code"]

        # Теперь обновляем его
        update_response = await ac.put(
            f"/{code}", json={"original_url": "https://example.com/updated"}
        )
        assert update_response.status_code == 200
        assert update_response.json()["original_url"] == "https://example.com/updated"

        # Проверяем, что редирект работает на новый URL
        redirect_response = await ac.get(f"/{code}", follow_redirects=False)
        assert redirect_response.status_code == 307
        assert redirect_response.headers["location"] == "https://example.com/updated"


@pytest.mark.asyncio
async def test_update_nonexistent_short_url():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.put(
            "/nonexistentcode", json={"original_url": "https://example.com"}
        )
    assert response.status_code == 404
    assert response.json() == {"detail": "Короткий URL не найден"}


@pytest.mark.asyncio
async def test_delete_short_url():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        # Сначала создаем короткий URL
        response = await ac.post(
            "/shorten", json={"original_url": "https://example.com/to-be-deleted"}
        )
        assert response.status_code == 200
        code = response.json()["code"]

        # Теперь удаляем его
        delete_response = await ac.delete(f"/{code}")
        assert delete_response.status_code == 200
        assert delete_response.json() == {"message": "URL удален успешно"}

        # Проверяем, что редирект теперь не работает
        redirect_response = await ac.get(f"/{code}")
        assert redirect_response.status_code == 404


@pytest.mark.asyncio
async def test_delete_nonexistent_short_url():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.delete("/nonexistentcode")
    assert response.status_code == 404
    assert response.json() == {"detail": "Короткий URL не найден"}
