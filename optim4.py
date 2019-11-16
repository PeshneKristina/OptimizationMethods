import math
from sympy import *
import math

x1, x2 = symbols('x1 x2')

eps = 0.01
delta = 0.001


# возвращает значение функции
def f1(x1, x2):
    return 100 * (x2 - x1 ** 2) ** 2 + 5 * (1 - x1) ** 2


# возвращает значение функции
def f2(x1, x2):
    return (x1 ** 2 + x2 - 11) ** 2 + (x1 + x2 ** 2 - 7) ** 2


# вычисляет производную функции по заданной переменной
def get_diff_f(f, x):
    return diff(f, x)


# вычисляет проивзодную функции в точке
def get_diff_f_in_point(x, y, func):
    f = lambdify([x1, x2], func, 'numpy')
    return f(x, y)


# возвращает норму двух векторов
def get_norm(x, y):
    return math.sqrt(x ** 2 + y ** 2)


# вспомогательная функция для выбора направления спуска методом дихотомии
def helper_function(f, x, y, alpha):
    return f(x - alpha * get_diff_f_in_point(x, y, get_diff_f(f(x1, x2), x1)),
             y - alpha * get_diff_f_in_point(x, y, get_diff_f(f(x1, x2), x2)))


# метод дихотомии
# метод половинного деления для нахождения минимума в градиентном спуске
def dihotomia(f, leftPoint, rightPoint, x, y):
    midPoint = average(leftPoint, rightPoint)
    if closeEnough(leftPoint, rightPoint):
        return midPoint
    # находим значения функции слева и справа от середины
    g1 = helper_function(f, x, y, midPoint - delta)
    g2 = helper_function(f, x, y, midPoint + delta)
    # отсекаем тот промежуток, где значение функции больше
    if g1 < g2:
        # print(
        #    "левый конец интервала: {0} , правый конец интервала: {1}.".format(
        #       leftPoint, midPoint))
        return dihotomia(f, leftPoint, midPoint, x, y)

    elif g1 > g2:
        # print(
        #    "левый конец интервала: {0}, правый конец интервала: {1}.".format(
        #        midPoint, rightPoint))
        return dihotomia(f, midPoint, rightPoint, x, y)
    return midPoint


# возвращает среднее значение
def average(x, y):
    return (x + y) / 2


# проверяет на близость значения
def closeEnough(x, y):
    if abs(x - y) < eps:
        return 1
    return 0


# метод наискорейшего спуска
def greatDescent(f, bx, by):
    # начальное приближение
    # Находим alpha_k как минимум вспомогательной функции на отрезке -10000,100000
    alpha = dihotomia(f, -10000, 100000, bx, by)
    x = bx - alpha * get_diff_f_in_point(bx, by, get_diff_f(f(x1, x2), x1))
    y = by - alpha * get_diff_f_in_point(bx, by, get_diff_f(f(x1, x2), x2))
    # Проверяем условие остановки
    list_comditions = []
    list_comditions.append(get_norm(x - bx, y - by))
    list_comditions.append(get_norm(f(x, y), f(bx, by)))
    list_comditions.append(
        get_norm(get_diff_f_in_point(x, y, get_diff_f(f1(x1, x2), x1)),
                 get_diff_f_in_point(x, y, get_diff_f(f1(x1, x2), x2))))
    print(list_comditions)
    print(x, y)
    if max(list_comditions) < eps:
        return [x, y]

    greatDescent(f, x, y)


def main():
    print(greatDescent(f1, -2.048, 2.048))


main()
