"""Расчёт базовых статистических показателей."""

from typing import Dict, Sequence


def _ensure_not_empty(data: Sequence[float]) -> None:
    """Проверяет, что ряд не пустой."""
    if not data:
        raise ValueError("Ряд пуст: расчёт статистики невозможен")


def mean(data: Sequence[float]) -> float:
    """Вычисляет среднее арифметическое."""
    _ensure_not_empty(data)
    return sum(data) / len(data)


def median(data: Sequence[float]) -> float:
    """Вычисляет медиану ряда."""
    _ensure_not_empty(data)
    values = sorted(data)
    middle = len(values) // 2
    if len(values) % 2:
        return float(values[middle])
    return (values[middle - 1] + values[middle]) / 2.0


def spread(data: Sequence[float]) -> float:
    """Вычисляет размах ряда."""
    _ensure_not_empty(data)
    return float(max(data) - min(data))


def summarize(data: Sequence[float]) -> Dict[str, float]:
    """Возвращает сводный отчёт по ряду."""
    _ensure_not_empty(data)
    return {
        "count": len(data),
        "mean": mean(data),
        "median": median(data),
        "spread": spread(data),
        "min": float(min(data)),
        "max": float(max(data)),
    }
