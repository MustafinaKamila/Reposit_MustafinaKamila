"""Журналирование ошибок пользовательского ввода."""

import datetime

from constants import LOG_FILE

_entries: list[str] = []


def log_error(message: str) -> None:
    """Добавляет сообщение об ошибке в память и файл."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {message}"
    _entries.append(entry)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as file:
            file.write(entry + "\n")
    except OSError:
        pass


def get_entries() -> list[str]:
    """Возвращает копию журнала ошибок."""
    return list(_entries)


def clear() -> None:
    """Очищает журнал ошибок в памяти."""
    _entries.clear()
