"""Дополнительные функции для варианта 14."""

import random
from typing import List, Optional, Sequence

from .stats import median


def triangular_series(
    n: int,
    seed: Optional[int] = None,
) -> List[float]:
    """Создаёт ряд из сумм двух равномерно распределённых чисел."""
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise ValueError("n должно быть положительным целым числом")

    rng = random.Random(seed)

    return [
        rng.uniform(0, 50) + rng.uniform(0, 50)
        for _ in range(n)
    ]


def median_absolute_deviation(data: Sequence[float]) -> float:
    """Вычисляет MAD — медиану абсолютных отклонений."""
    if not data:
        raise ValueError("Ряд пуст")

    center = median(data)

    deviations = [
        abs(value - center)
        for value in data
    ]

    return median(deviations)


def weighted_moving_average(
    data: Sequence[float],
    window: int,
) -> List[float]:
    """Вычисляет WMA с линейными весами от 1 до window."""
    if not data:
        raise ValueError("Ряд пуст")

    if (
        not isinstance(window, int)
        or isinstance(window, bool)
        or window < 1
        or window > len(data)
    ):
        raise ValueError(
            "window должно быть целым числом от 1 до длины ряда"
        )

    weight_sum = window * (window + 1) / 2
    result = []

    for start in range(len(data) - window + 1):
        weighted_sum = 0.0

        for j in range(window):
            weight = j + 1
            weighted_sum += data[start + j] * weight

        result.append(weighted_sum / weight_sum)

    return result