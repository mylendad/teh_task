from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from app import schemas
from app.services import shortener_service
from app.exceptions import ShortCodeCollisionException, ShortUrlNotFoundException
import logging

router = APIRouter()

@router.post("/shorten", response_model=schemas.URLInfo)
def create_short_url(url: schemas.URLCreate):
    """
    Создать короткий URL.
    """
    logging.info(f"Получен запрос на сокращение URL: {url.original_url}")
    try:
        short_code = shortener_service.create_short_url(str(url.original_url))
        return schemas.URLInfo(original_url=url.original_url, code=short_code)
    except Exception as e:
        logging.error(f"Не удалось создать короткий URL: {e}")
        raise ShortCodeCollisionException()

@router.get("/{code}")
def redirect_to_original_url(code: str):
    """
    Перенаправить на оригинальный URL.
    """
    logging.info(f"Получен запрос на перенаправление для кода: {code}")
    original_url = shortener_service.get_original_url(code)
    if original_url:
        logging.info(f"Перенаправление на: {original_url}")
        return RedirectResponse(url=original_url, status_code=307)
    else:
        logging.warning(f"Короткий код не найден: {code}")
        raise ShortUrlNotFoundException()

@router.put("/{code}", response_model=schemas.URLInfo)
def update_short_url(code: str, url: schemas.URLUpdate):
    """
    Обновить оригинальный URL для короткого кода.
    """
    logging.info(f"Получен запрос на обновление URL для кода: {code}")
    success = shortener_service.update_original_url(code, str(url.original_url))
    if success:
        logging.info(f"URL для кода {code} успешно обновлен на: {url.original_url}")
        return schemas.URLInfo(original_url=url.original_url, code=code)
    else:
        logging.warning(f"Короткий код не найден для обновления: {code}")
        raise ShortUrlNotFoundException()

@router.delete("/{code}")
def delete_short_url(code: str):
    """
    Удалить короткий URL.
    """
    logging.info(f"Получен запрос на удаление URL для кода: {code}")
    success = shortener_service.delete_url(code)
    if success:
        logging.info(f"URL для кода {code} успешно удален.")
        return JSONResponse(status_code=200, content={"message": "URL удален успешно"})
    else:
        logging.warning(f"Короткий код не найден для удаления: {code}")
        raise ShortUrlNotFoundException()
