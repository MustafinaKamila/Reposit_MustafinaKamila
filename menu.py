"""Меню выбора материала для варианта 14."""

from constants import K_ALUMINUM, K_CAST_IRON, K_STEEL


def show_menu() -> None:
    """Выводит меню выбора материала."""
    print("\nВыберите материал:")
    print("1 — сталь (V = 80 м/мин)")
    print("2 — алюминий (V = 250 м/мин)")
    print("3 — чугун (V = 60 м/мин)")
    print("0 — выход")


def select_mode() -> float | None:
    """Запрашивает материал и возвращает его скорость резания."""
    while True:
        choice = input("Введите номер материала (0–3): ").strip()
        match choice:
            case "1":
                return K_STEEL
            case "2":
                return K_ALUMINUM
            case "3":
                return K_CAST_IRON
            case "0":
                return None
            case _:
                print("Ошибка: неверный пункт меню. Повторите ввод.")


def mode_name(v: float) -> str:
    """Возвращает название материала по скорости резания."""
    match v:
        case 80.0:
            return "сталь"
        case 250.0:
            return "алюминий"
        case 60.0:
            return "чугун"
        case _:
            return "неизвестный материал"
