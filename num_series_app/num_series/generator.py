"""Формирование числовых рядов."""

import math
import random
from typing import List, Optional


def _validate_n(n: int) -> None:
    """Проверяет, что n является положительным целым числом."""
    try:
        is_positive_int = n > 0 and int(n) == n
    except (TypeError, ValueError) as err:
        raise ValueError(
            f"n должно быть положительным целым числом "
            f"(получено: {n!r}; причина: {err.args[0]})"
        ) from err
    if not is_positive_int:
        raise ValueError(f"n должно быть положительным целым числом (получено: {n!r})")


def random_series(n: int, low: float = -100.0, high: float = 100.0,
                  seed: Optional[int] = None) -> List[float]:
    """Возвращает ряд случайных чисел на отрезке [low, high]."""
    _validate_n(n)
    if low >= high:
        raise ValueError(f"low должно быть меньше high (получено: {low} >= {high})")
    rng = random.Random(seed)
    return [rng.uniform(low, high) for _ in range(n)]


def sine_series(n: int, amplitude: float = 1.0, frequency: float = 1.0,
                noise: float = 0.0, seed: Optional[int] = None) -> List[float]:
    """Возвращает синусоидальный ряд с добавочным шумом."""
    _validate_n(n)
    rng = random.Random(seed)
    return [
        amplitude * math.sin(2 * math.pi * frequency * i / n)
        + (rng.uniform(-noise, noise) if noise else 0.0)
        for i in range(n)
    ]


def trend_series(n: int, start: float = 0.0, step: float = 1.0,
                 noise: float = 0.0, seed: Optional[int] = None) -> List[float]:
    """Возвращает линейный тренд с добавочным шумом."""
    _validate_n(n)
    rng = random.Random(seed)
    return [
        start + step * i + (rng.uniform(-noise, noise) if noise else 0.0)
        for i in range(n)
    ]