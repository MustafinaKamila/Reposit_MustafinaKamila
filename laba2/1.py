import math

materials = {
    1: {'name': 'сталь', 'speed': 80},
    2: {'name': 'алюминий', 'speed': 250},
    3: {'name': 'чугун', 'speed': 60},
}

try:
    mat_choice = int(input('Выберите материал (1 — сталь, 2 — алюминий, 3 — чугун): '))
    if mat_choice not in materials:
        raise ValueError('Нужно выбрать материал: 1, 2 или 3.')

    D = float(input('Введите диаметр фрезы D (мм): '))
    Z = int(input('Введите число зубьев Z: '))
    Sz = float(input('Введите подачу на зуб Sz (мм/зуб): '))
    t = float(input('Введите глубину резания t (мм): '))
    if not all(math.isfinite(value) and value > 0 for value in (D, Z, Sz, t)):
        raise ValueError('Все параметры должны быть положительными конечными числами.')
except ValueError as error:
    print(f'Ошибка ввода: {error}')
    raise SystemExit(1)

material_name = materials[mat_choice]['name']
V = materials[mat_choice]['speed']

n = 1000 * V / (math.pi * D)
Smin = Sz * Z * n
# Сохраняем предположение исходной программы: ширина фрезерования равна D/2.
MRR = t * (D / 2) * Smin / 1000

# Предполагаемые границы: до 1 мм, от 1 до 3 мм и больше 3 мм.
if t < 1:
    proc_type = 'чистовая'
elif t <= 3:
    proc_type = 'получистовая'
else:
    proc_type = 'черновая'

print('\n--- Результаты расчета ---')
print(f'Материал: {material_name}')
print(f'Частота вращения (n): {n:.2f} об/мин')
print(f'Минутная подача (Smin): {Smin:.2f} мм/мин')
print(f'Объем снимаемого материала (MRR): {MRR:.2f} см³/мин')
print(f'Тип обработки: {proc_type}')
