import math
from sympy import *

x1, x2 = symbols('x1 x2')

eps = 0.005
delta = 0.0001


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
        return dihotomia(f, leftPoint, midPoint + delta, x, y)

    elif g1 > g2:
        # print(
        #    "левый конец интервала: {0}, правый конец интервала: {1}.".format(
        #        midPoint, rightPoint))
        return dihotomia(f, midPoint - delta, rightPoint, x, y)
    return midPoint


# возвращает среднее значение
def average(x, y):
    return (x + y) / 2


# проверяет на близость значения
def closeEnough(x, y):
    if abs(x - y) < 0.001:
        return 1
    return 0


# метод наискорейшего спуска
def greatDescent(f, x0, y0):
    # выбираем начальное приближение
    print("x0,yo ", x0, y0)
    # Находим alpha_ как минимум вспомогательной функции на отрезке 0,100000
    alpha = dihotomia(f, 0, 100000, x0, y0)
    x = x0 - alpha * get_diff_f_in_point(x0, y0, get_diff_f(f(x1, x2), x1))
    y = y0 - alpha * get_diff_f_in_point(x0, y0, get_diff_f(f(x1, x2), x2))
    print("x,y", x, y)
    # Проверяем условие остановки
    print("norma,eps",get_norm(x - x0, y - y0),eps)
    if get_norm(x - x0, y - y0) < eps:
        return [x, y]
    return greatDescent(f, x, y)


def main():
    print("Метод наискорейшего спуска для f1")
    min1 = greatDescent(f1, 0.5, 1.5)
    print("Метод наискорейшего спуска для f2")
    min2 = greatDescent(f2, -2.048, 2.048)
    print("точка минимума f1: ", min1)
    print("минимум f1: ", f1(min1[0], min1[1]))
    print("точка минимума f2: ", min2)
    print("минимум f1: ", f2(min2[0], min2[1]))


main()
