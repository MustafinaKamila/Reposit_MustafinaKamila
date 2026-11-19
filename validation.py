"""Проверка и циклический ввод данных варианта 14."""

from constants import D_MAX, D_MIN, SZ_MAX, SZ_MIN, T_MAX, T_MIN, Z_MAX, Z_MIN
from logger import log_error


def validate_range(value: float, low: float, high: float) -> tuple[bool, str]:
    """Проверяет попадание значения в допустимый диапазон."""
    if value < low:
        return False, f"Ошибка: значение меньше нижней границы ({low})"
    elif value > high:
        return False, f"Ошибка: значение больше верхней границы ({high})"
    else:
        return True, ""


def input_number(prompt: str, low: float, high: float) -> float:
    """Циклически запрашивает число до получения корректного значения."""
    while True:
        raw = input(prompt).strip()
        try:
            value = float(raw)
        except ValueError:
            message = f"Ошибка: введено не число ({raw!r})."
            print(message)
            log_error(message)
            continue

        valid, message = validate_range(value, low, high)
        if valid:
            return value
        print(message + ". Повторите ввод.")
        log_error(message)


def input_diameter() -> float:
    """Запрашивает диаметр фрезы D от 5 до 200 мм."""
    return input_number("Введите диаметр фрезы D (5..200 мм): ", D_MIN, D_MAX)


def input_chiszub() -> float:
    """Запрашивает число зубьев z от 1 до 20."""
    return input_number("Введите число зубьев z (1..20): ", Z_MIN, Z_MAX)


def input_podzub() -> float:
    """Запрашивает подачу на зуб Sz от 0.01 до 0.5 мм/зуб."""
    return input_number("Введите подачу на зуб Sz (0.01..0.5): ", SZ_MIN, SZ_MAX)


def input_glubrez() -> float:
    """Запрашивает глубину резания t от 0.1 до 10 мм."""
    return input_number("Введите глубину резания t (0.1..10 мм): ", T_MIN, T_MAX)
