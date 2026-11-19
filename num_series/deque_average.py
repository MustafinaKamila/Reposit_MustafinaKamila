from __future__ import annotations
import math
from collections import deque
from typing import Deque, Iterable, List, Sequence

#Валидация(единая точка отказа-fail fast)
def _ensure_not_empty(data: Sequence[float]) -> None:
    if not data:
        raise ValueError("Ряд пуст: расчёт скользящей средней невозможен")
def _check_window(window: int, n: int) -> None:
    if not isinstance(window, int) or isinstance(window, bool):
        raise ValueError(f"window должен быть целым, получено: {window!r}")
    if window < 1:
        raise ValueError(f"window должен быть >= 1, получено: {window}")
    if window > n:
        raise ValueError(
            f"window ({window}) больше длины ряда ({n}) — SMA невозможна"
        )
def _check_alpha(alpha: float) -> None:
    if not (0 < alpha <= 1):
        raise ValueError(f"alpha должен быть в (0, 1], получено: {alpha}")

#Простая скользящая средняя(SMA) через deque
def simple_moving_average_deque(
    data: Sequence[float],
    window: int,
) -> List[float]:
    _ensure_not_empty(data)
    _check_window(window, len(data))
    buf: Deque[float] = deque(maxlen=window)
    running = 0.0
    result: List[float] = []
    for i, x in enumerate(data):
        if len(buf) == window:
            running -= buf[0]
        buf.append(x)
        running += x
        if i >= window - 1:
            result.append(running / window)
    return result

#Центрированное MA через deque
def centered_moving_average_deque(
    data: Sequence[float],
    window: int,
) -> List[float]:
    _ensure_not_empty(data)
    _check_window(window, len(data))
    if window % 2 == 0:
        raise ValueError(
            f"Центрированное MA требует нечётного window, получено: {window}"
        )
           
    half = window // 2
    buf: Deque[float] = deque(maxlen=window)
    running = 0.0
    result: List[float] = []

    for x in data:
        if len(buf) == window:
            running -= buf[0]
        buf.append(x)
        running += x
        # Индекс «центра» окна в исходном ряду:
        # после append deque заполнен, len(buf) == window, центр = half
        # Если окно ещё не набрано — пропускаем.
        if len(buf) == window:
            result.append(running / window)
    #Экспоненциальная скользящая средняя (EMA) через deque
    def exponential_moving_average_deque(
        data: Sequence[float],
        alpha: float,
    ) -> List[float]:
        """EMA:
    EMA[0] = data[0];
    EMA[i] = alpha*data[i] + (1-alpha)*EMA[i-1].
        deque нужен только как ring-buffer истории (для отладки/расширений);
        в классической EMA достаточно одной переменной. Здесь оставлен
        для симметрии с SMA и чтобы показать потоковый характер.
        """
        _ensure_not_empty(data)
        _check_alpha(alpha)

        buf: Deque[float] = deque(maxlen=1)
        prev: float = float(data[0])
        result: List[float] = [prev]

        for x in data[1:]:
            prev = alpha * x + (1.0 - alpha) * prev
            result.append(prev)
            buf.append(prev) # ring-buffer последнего значения (для потокового API)
        return result

        #Публичный список того, что отдает модуль
        __all__ = [
            "simple_moving_average_deque",
            "centered_moving_average_deque",
            "exponential_moving_average_deque",
        ]