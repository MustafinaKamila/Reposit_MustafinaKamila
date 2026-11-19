"""Алгоритмы простого, центрированного и экспоненциального сглаживания."""

from typing import List, Sequence


def _check_window(window: int, n: int) -> None:
    """Проверяет размер окна."""
    if window < 1 or window > n:
        raise ValueError("window должно быть от 1 до длины ряда")


def simple_moving_average(data: Sequence[float], window: int) -> List[float]:
    """Вычисляет простую скользящую среднюю за O(n)."""
    if not data:
        raise ValueError("Ряд пуст")
    _check_window(window, len(data))
    running = sum(data[:window])
    result = [running / window]
    for i in range(window, len(data)):
        running += data[i] - data[i - window]
        result.append(running / window)
    return result


def centered_moving_average(data: Sequence[float], window: int) -> List[float]:
    """Вычисляет центрированную среднюю для нечётного окна."""
    if window % 2 == 0:
        raise ValueError("Для центрированной средней окно должно быть нечётным")
    return simple_moving_average(data, window)


def exponential_moving_average(data: Sequence[float], alpha: float) -> List[float]:
    """Вычисляет экспоненциальную скользящую среднюю."""
    if not data:
        raise ValueError("Ряд пуст")
    if not 0 < alpha <= 1:
        raise ValueError("alpha должно быть больше 0 и не больше 1")
    result = [float(data[0])]
    for value in data[1:]:
        result.append(alpha * value + (1 - alpha) * result[-1])
    return result
