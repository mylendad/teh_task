import sqlite3

import shortuuid


def create_short_url(db: sqlite3.Connection, original_url: str) -> str:
    """
    Создает короткий URL для данного оригинального URL.

    Args:
        db: Соединение с базой данных.
        original_url: Оригинальный URL для сокращения.

    Returns:
        Короткий код для URL.

    Raises:
        Exception: Если не удалось создать уникальный короткий код.
    """
    cursor = db.execute("SELECT code FROM urls WHERE original_url = ?", (original_url,))
    row = cursor.fetchone()
    if row:
        return row["code"]

    for _ in range(10):
        code = shortuuid.uuid()[:8]
        try:
            db.execute(
                "INSERT INTO urls (original_url, code) VALUES (?, ?)",
                (original_url, code),
            )
            db.commit()
            return code
        except sqlite3.IntegrityError:
            # Это может произойти, если сгенерированный код уже существует.
            # Цикл попробует снова с новым кодом.
            continue

    raise Exception("Не удалось создать уникальный короткий код после 10 попыток.")


def get_original_url(db: sqlite3.Connection, code: str) -> str | None:
    """
    Получает оригинальный URL для данного короткого кода.

    Args:
        db: Соединение с базой данных.
        code: Короткий код.

    Returns:
        Оригинальный URL или None, если не найден.
    """
    cursor = db.execute("SELECT original_url FROM urls WHERE code = ?", (code,))
    row = cursor.fetchone()
    if row:
        return row["original_url"]
    return None


def update_original_url(
    db: sqlite3.Connection, code: str, new_original_url: str
) -> bool:
    """
    Обновляет оригинальный URL для данного короткого кода.

    Args:
        db: Соединение с базой данных.
        code: Короткий код.
        new_original_url: Новый оригинальный URL.

    Returns:
        True, если обновление прошло успешно, иначе False.
    """
    cursor = db.execute(
        "UPDATE urls SET original_url = ? WHERE code = ?",
        (new_original_url, code),
    )
    db.commit()
    return cursor.rowcount > 0


def delete_url(db: sqlite3.Connection, code: str) -> bool:
    """
    Удаляет URL по короткому коду.

    Args:
        db: Соединение с базой данных.
        code: Короткий код.

    Returns:
        True, если удаление прошло успешно, иначе False.
    """
    cursor = db.execute("DELETE FROM urls WHERE code = ?", (code,))
    db.commit()
    return cursor.rowcount > 0
