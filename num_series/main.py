"""Точка входа приложения обработки числовых рядов."""

from __future__ import annotations
import argparse
import csv
import json
import sys
from typing import List, Optional, Tuple
from num_series import (
    random_series, sine_series, trend_series, summarize,
    simple_moving_average, centered_moving_average, exponential_moving_average,
    save_series_json, load_series_auto, benchmark_moving_average,
)
from num_series.variant14 import (
    triangular_series,
    median_absolute_deviation,
    weighted_moving_average,
)

from num_series.moving_average import simple_moving_average_deque

#Источники данных
def build_series(kind: str, n: int, seed: int) -> List[float]:
    """Создаёт ряд выбранного типа."""
    if kind == "triangular":
        return triangular_series(n, seed=seed)

    if kind == "random":
        return random_series(n, low=-50, high=50, seed=seed)

    if kind == "sine":
        return sine_series(n,amplitude=10,frequency=2,noise=1.5,seed=seed,)

    if kind == "trend":
        return trend_series(n,start=0,step=1,noise=0.5,seed=seed,)

    raise ValueError(f"Неизвестный тип ряда: {kind}")

def obtain_series(args: argparse.Namespace) -> Tuple[List[float], str]:
    """Возвращает (ряд, описание источника)."""
    if args.load:
        data = load_series_auto(args.load)
        return data, f"файл: {args.load}"
    data = build_series(args.kind, args.n, args.seed)
    return data, f"сгенерирован ({args.kind}, n={args.n}, seed={args.seed})"

#Экспорт в CSV
def export_series_csv(path: str, data: List[float]) -> None:
    """Экспорт ряда в CSV: столбцы i, value. Ошибки нормализуются в ValueError."""
    try:
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["i", "value"])
            for i, v in enumerate(data):
                w.writerow([i, v])
    except OSError as err:
        raise ValueError(f"Не удалось записать CSV {path}: {err}") from err


#Печать 
def print_series(title: str, values: List[float], fmt: str = "{:>10.3f}") -> None:
    """Печатает ряд в одну строку с выравниванием."""
    print(f"\n{title} (n={len(values)}):")
    print(" " + " ".join(fmt.format(v) for v in values))

def print_header(source: str) -> None:
    print("=" * 60)
    print(f"Источник данных: {source}")
    print("-" * 60)

def print_stats(stats: dict) -> None:
    """Печатает блок базовых статистических показателей."""
    print(f"Среднее арифметическое : {stats['mean']:>10.4f}")
    print(f"Медиана : {stats['median']:>10.4f}")
    print(f"Размах (max - min) : {stats['spread']:>10.4f}")
    print(f"min / max : {stats['min']:>10.4f} / {stats['max']:.4f}")

def print_footer() -> None:
    print("=" * 60)

#CLI
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Алгоритмическая обработка числовых рядов",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog="Пример: python main.py --kind sine --n 20 --save data/s.json",
    )
    # источники
    parser.add_argument("--kind",choices=["random", "sine", "trend", "triangular"],default="triangular",
        help="тип генерируемого ряда",)
    parser.add_argument("--n",type=int,default=1000,
        help="количество чисел в ряде",)
    parser.add_argument("--seed", type=int, default=42,
        help="зерно ГПСЧ для воспроизводимости")
    parser.add_argument("--load", metavar="PATH",
        help="загрузить ряд из файла (.json/.txt/.csv); "
            "отменяет --kind/--n/--seed")
    # экспорт
    parser.add_argument("--save", metavar="PATH",
        help="сохранить ряд в JSON-файл")
    parser.add_argument("--export", metavar="FILE",
        help="экспортировать ряд в CSV (i, value)")
    # анализ
    parser.add_argument("--window",type=int,default=10,
        help="размер окна",)
    parser.add_argument("--alpha", type=float, default=0.3,
        help="коэффициент сглаживания для EMA, 0 < alpha <= 1")
    parser.add_argument(
        "--benchmark",
        action="store_true",
        help="замерить время выполнения SMA для list и deque",
    )
    
    return parser

def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    #---1.Получаем ряд---
    try:
        data, source = obtain_series(args)
    except ValueError as err:
        print(f"Ошибка получения ряда: {err}", file=sys.stderr)
        return 1
    # --- 2. Сохраняем (до анализа — данные на диске даже при ошибке анализа) ---
    if args.save:
        meta = {"source": source}
        if not args.load:
            meta.update({"kind": args.kind, "seed": args.seed})
        try:
            save_series_json(data, args.save, meta=meta)
            print(f"[сохранено] {args.save} ({len(data)} точек)")
        except ValueError as err:
            print(f"Ошибка сохранения: {err}", file=sys.stderr)
            return 1
    if args.export:
        try:
            export_series_csv(args.export, data)
            print(f"[экспортировано] {args.export} ({len(data)} точек)")
        except ValueError as err:
            print(f"Ошибка экспорта: {err}", file=sys.stderr)
            return 1

        # --- 3. Анализ ---
    try:
        stats = summarize(data)
        mad_value = median_absolute_deviation(data)
        sma = simple_moving_average(data, args.window)
        sma_deque = simple_moving_average_deque(data,args.window,)
        wma = weighted_moving_average(data,args.window,)
    except ValueError as err:
        print(f"Ошибка анализа: {err}", file=sys.stderr)
        return 1

    # --- 4. Вывод ---
    print_header(source)
    print_stats(stats)

    print(f"MAD: {mad_value:.4f}")

    print_series("Исходный ряд", data)

    print_series(f"SMA list (window={args.window})",sma,)

    print_series(f"SMA deque (window={args.window})",sma_deque,)

    print_series(f"WMA (window={args.window})",wma,)
    if args.benchmark:
        print("-" * 60)
        print(
        "Замер времени выполнения SMA "
        "(среднее за 1000 повторов):"
        )
        timings = benchmark_moving_average(data,args.window,repeats=1000,)
        print(f"  list  : {timings['list']:.8f} с")
        print(f"  deque : {timings['deque']:.8f} с")
        print("  отношение (list/deque):"
              f"{timings['list'] / timings['deque']:.2f}")
    print_footer()
    return 0

if __name__ == "__main__":
        raise SystemExit(main())