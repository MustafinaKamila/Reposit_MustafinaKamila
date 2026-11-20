"""Расчёты режимов фрезерования для варианта 14."""

import math


def cutting_speed(v: float, d: float) -> float:
    """Вычисляет частоту вращения фрезы n.

    Args:
        v: скорость резания, м/мин.
        d: диаметр фрезы, мм.

    Returns:
        Частота вращения, об/мин.
    """

    return 1000 * v / (math.pi * d)


def feed_per_minute(sz: float, z: float, n: float) -> float:
    """Вычисляет минутную подачу.

    Args:
        sz: подача на один зуб, мм/зуб.
        z: число зубьев.
        n: частота вращения, об/мин.

    Returns:
        Минутная подача, мм/мин.
    """

    return sz * z * n


def material_removal_rate(t: float, d: float, s_min: float) -> float:
    """Вычисляет производительность удаления материала.

    Args:
        t: глубина резания, мм.
        d: диаметр фрезы, мм.
        s_min: минутная подача, мм/мин.

    Returns:
        Производительность, см3/мин.
    """

    return t * (d / 2) * s_min / 1000


def depth_class(t: float) -> str:
    """Определяет тип обработки по глубине резания.

    Args:
        t: глубина резания, мм.

    Returns:
        Название типа обработки.
    """

    if t < 1:
        return "чистовая"
    elif t <= 3:
        return "получистовая"
    else:
        return "черновая"