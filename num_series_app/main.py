"""Точка входа приложения обработки числовых рядов."""

import argparse
import sys

from num_series import (
    random_series, sine_series, trend_series, summarize,
    simple_moving_average, centered_moving_average, exponential_moving_average,
)

def build_series(kind: str, n: int, seed: int):
    """Формирует ряд выбранного типа."""
    if kind == "random":
        return random_series(n, low=-50, high=50, seed=seed)
    if kind == "sine":
        return sine_series(n, amplitude=10, frequency=2, noise=1.5, seed=seed)
    if kind == "trend":
        return trend_series(n, start=0, step=1, noise=0.5, seed=seed)
    raise ValueError(f"Неизвестный тип ряда: {kind}")

def build_parser():
    """Создаёт парсер аргументов командной строки."""
    parser = argparse.ArgumentParser(description="Обработка числовых рядов")
    parser.add_argument("--kind", choices=["random", "sine", "trend"], default="sine")
    parser.add_argument("--n", type=int, default=20)
    parser.add_argument("--window", type=int, default=3)
    parser.add_argument("--alpha", type=float, default=0.3)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--export",metavar="FILE",help="экспорт в CSV")
    return parser

#main()

def main(argv=None) -> int:
    """Запускает генерацию, анализ и вывод результата."""
    args = build_parser().parse_args(argv)
    try:
        data = build_series(args.kind, args.n, args.seed)
        result = summarize(data)
        sma = simple_moving_average(data, args.window)
        ema = exponential_moving_average(data, args.alpha)
        cma = centered_moving_average(data, args.window) if args.window % 2 else None
    except ValueError as err:
        print(f"Ошибка: {err}", file=sys.stderr)
        return 1
    print(f"Среднее: {result['mean']:.4f}")
    print(f"Медиана: {result['median']:.4f}")
    print(f"Размах: {result['spread']:.4f}")
    print(f"SMA: {sma}")
    print(f"EMA: {ema}")
    if cma is not None:
        print(f"Центрированное MA: {cma}")

    print()

#В main()
    if args.export:
        import csv
        with open(args.export,"w",newlinw="",encoding="utf-8")as f:
            w=csv.writer(f)
            w.writerow(["i","value"])
            for i,v in enumerate(data):
                w.writerow([i,v])
        print(f"Экспортировано в {args.export}")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())