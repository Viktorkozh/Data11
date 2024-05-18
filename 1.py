#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 9
# С использованием многопоточности для заданного значения x найти сумму ряда S
# с точностью члена ряда по абсолютному значению e=10^-7 и произвести
# сравнение полученной суммы с контрольным значением функции y для двух
# бесконечных рядов.
# Варианты 16 и 17

# 11
# Для своего индивидуального задания лабораторной работы 2.23 необходимо
# реализовать вычисление значений в двух функций в отдельных процессах.

import math
from multiprocessing import Process, Array, Manager

epsilon = 1e-7


def power(x, n, cache):
    if (x, n) not in cache:
        cache[(x, n)] = x**n
    return cache[(x, n)]


def func(x, result, cache):
    sum = 0
    n = 0
    term = 1
    factor = 1
    while abs(term) > epsilon:
        sum += term
        n += 1
        factor *= n
        term = (-1)**n * power(x, 2 * n, cache) / factor
    result[0] = sum


def func2(x, result, cache):
    sum = 0
    n = 1
    while True:
        term = 1 / (2 * n - 1) * power((x - 1) / (x + 1), 2 * n - 1, cache)
        if abs(term) < epsilon:
            break
        else:
            sum += term
            n += 1
    result[1] = sum


def main():
    result = Array('d', [0.0, 0.0])

    process1 = Process(target=func, args=(-0.7, result, cache))
    process2 = Process(target=func2, args=(0.6, result, cache))

    process1.start()
    process2.start()

    process1.join()
    process2.join()

    sum_func = result[0]
    sum_func2 = result[1]

    test1 = math.exp(-(-0.7)**2)
    test2 = 1/2 * math.log(0.6)

    print(f"Результат функции 1: {sum_func}")
    print(f"Контрольное значение для функции 1: {test1}")
    print(f"Результат функции 2: {sum_func2}")
    print(f"Контрольное значение для функции 2: {test2}")

    if abs(sum_func - test1) < epsilon:
        print("func: Верно.")
    else:
        print("func: Неверно.")

    if abs(sum_func2 - test2) < epsilon:
        print("series_solution: Верно.")
    else:
        print("series_solution: Неверно.")


if __name__ == "__main__":
    manager = Manager()
    cache = manager.dict()
    main()
