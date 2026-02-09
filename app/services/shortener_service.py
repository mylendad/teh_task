import sqlite3

import shortuuid

from app import database


def create_short_url(original_url: str) -> str:
    """
    Создает короткий URL для данного оригинального URL.

    Args:
        original_url: Оригинальный URL для сокращения.

    Returns:
        Короткий код для URL.

    Raises:
        Exception: Если не удалось создать уникальный короткий код.
    """
    conn = database.get_db_connection()
    try:
        cursor = conn.execute(
            "SELECT code FROM urls WHERE original_url = ?", (original_url,)
        )
        row = cursor.fetchone()
        if row:
            return row["code"]

        for _ in range(10):
            code = shortuuid.uuid()[:8]
            try:
                conn.execute(
                    "INSERT INTO urls (original_url, code) VALUES (?, ?)",
                    (original_url, code),
                )
                conn.commit()
                return code
            except sqlite3.IntegrityError:
                continue
    finally:
        conn.close()

    raise Exception("Не удалось создать уникальный короткий код.")


def get_original_url(code: str) -> str | None:
    """
    Получает оригинальный URL для данного короткого кода.

    Args:
        code: Короткий код.

    Returns:
        Оригинальный URL или None, если не найден.
    """
    conn = database.get_db_connection()
    cursor = conn.execute("SELECT original_url FROM urls WHERE code = ?", (code,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return row["original_url"]
    return None


def update_original_url(code: str, new_original_url: str) -> bool:
    """
    Обновляет оригинальный URL для данного короткого кода.

    Args:
        code: Короткий код.
        new_original_url: Новый оригинальный URL.

    Returns:
        True, если обновление прошло успешно, иначе False.
    """
    conn = database.get_db_connection()
    cursor = conn.execute(
        "UPDATE urls SET original_url = ? WHERE code = ?",
        (new_original_url, code),
    )
    conn.commit()
    conn.close()
    return cursor.rowcount > 0


def delete_url(code: str) -> bool:
    """
    Удаляет URL по короткому коду.

    Args:
        code: Короткий код.

    Returns:
        True, если удаление прошло успешно, иначе False.
    """
    conn = database.get_db_connection()
    cursor = conn.execute("DELETE FROM urls WHERE code = ?", (code,))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0
