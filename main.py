"""Точка входа приложения для расчёта режимов фрезерования."""

from menu import mode_name, select_mode, show_menu
from operations import cutting_speed, depth_class, feed_per_minute, material_removal_rate
from validation import input_chiszub, input_diameter, input_glubrez, input_podzub


def main() -> None:
    """Запускает главный цикл расчётов."""
    print("=== Расчёт режимов фрезерования, вариант 14 ===")

    while True:
        show_menu()
        V = select_mode()
        if V is None:
            print("Работа завершена.")
            break

        d = input_diameter()
        z = input_chiszub()
        sz = input_podzub()
        t = input_glubrez()

        n = cutting_speed(V, d)
        Smin = feed_per_minute(sz, z, n)
        MRR = material_removal_rate(t, d, Smin)
        processing_type = depth_class(t)

        print("\n=== Результаты расчёта ===")
        print(f"Материал: {mode_name(V)}")
        print(f"Скорость резания V: {V:.2f} м/мин")
        print(f"Частота вращения n: {n:.2f} об/мин")
        print(f"Минутная подача Sмин: {Smin:.2f} мм/мин")
        print(f"Производительность MRR: {MRR:.2f} см³/мин")
        print(f"Тип обработки: {processing_type}")


if __name__ == "__main__":
    main()
