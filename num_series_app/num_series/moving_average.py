"""Алгоритмы простого, центрированного и экспоненциального сглаживания."""

import time
from collections import deque
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

def simple_moving_average_deque(data: Sequence[float], window: int) -> List[float]:
    """SMA с использованием deque (двусторонней очереди)."""
    _check_window(window, len(data))
    result = []
    d = deque()
    running_sum = 0.0
    for x in data:
        d.append(x)
        running_sum += x
        if len(d) > window:
            running_sum -= d.popleft()
        if len(d) == window:
            result.append(running_sum / window)
    return result
def benchmark_moving_average(data: Sequence[float], window: int, repeats: int = 1000) -> dict:
    _check_window(window, len(data))
    t0 = time.perf_counter()
    for _ in range(repeats):
        simple_moving_average(data, window)
    t_list = (time.perf_counter() - t0) / repeats
    t0 = time.perf_counter()
    for _ in range(repeats):
        simple_moving_average_deque(data, window)
    t_deque = (time.perf_counter() - t0) / repeats

    return {"list": t_list, "deque": t_deque}