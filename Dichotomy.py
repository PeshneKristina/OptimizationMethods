# дихотомия

import math

eps = 0.001
delta = 0.0001


# возвращает значение функции
def f(x):
    a = 4
    b = 3
    return a * x + b / (math.exp(x))


# применяем метод дихотомии
def Dichotomy(leftPoint, rightPoint):
    # вычисляем середину отрезка
    midPoint = average(leftPoint, rightPoint)
    # проверяем условие остановки
    if closeEnough(leftPoint, rightPoint):
        return midPoint
    # находим значения функции слева и справа от середины
    f1 = f(midPoint - delta)
    f2 = f(midPoint + delta)
    # отсекаем тот промежуток, где значение функции больше
    if f1 < f2:
        print(
            "левый конец интервала: {0} , правый конец интервала: {1}.".format(
                leftPoint, midPoint))
        return Dichotomy(leftPoint, midPoint)

    elif f1 > f2:
        print(
            "левый конец интервала: {0}, правый конец интервала: {1}.".format(
                midPoint, rightPoint))
        return Dichotomy(midPoint, rightPoint)
    return midPoint


# возвращает среднее значение
def average(x, y):
    return (x + y) / 2


# проверяет на близость значения
def closeEnough(x, y):
    if abs(x - y) < eps:
        return 1
    return 0


def main():
    left_point = -1
    right_point = 1
    min = Dichotomy(left_point, right_point)
    print("точка минимума", min)
    print("минимум функции",f(min))


main()
