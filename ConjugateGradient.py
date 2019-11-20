from sympy import *

eps = 0.001
delta = 0.0001

x1, x2 = symbols('x1 x2')


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


# Вычисление скалярного произведения
def inner_product(x1, y1, x2, y2):
    return x1 * x2 + y1 * y2


# метод дихотомии
# метод половинного деления для нахождения минимума F1(x + alpha * p)
def dihotomia(f, leftPoint, rightPoint, x, y, p1, p2):
    midPoint = average(leftPoint, rightPoint)
    if closeEnough(leftPoint, rightPoint):
        return midPoint
    # находим значения функции слева и справа от середины
    x_g1 = x + (midPoint - delta) * p1
    y_g1 = y + (midPoint - delta) * p2
    x_g2 = x + (midPoint + delta) * p1
    y_g2 = y + (midPoint + delta) * p2
    g1 = f(x_g1, y_g1)
    g2 = f(x_g2, y_g2)
    # отсекаем тот промежуток, где значение функции больше
    if g1 < g2:
        # print(
        #    "левый конец интервала: {0} , правый конец интервала: {1}.".format(
        #       leftPoint, midPoint))
        return dihotomia(f, leftPoint, midPoint + delta, x, y,p1,p2)

    elif g1 > g2:
        # print(
        #    "левый конец интервала: {0}, правый конец интервала: {1}.".format(
        #        midPoint, rightPoint))
        return dihotomia(f, midPoint - delta, rightPoint, x, y,p1,p2)
    return midPoint


# возвращает среднее значение
def average(x, y):
    return (x + y) / 2


# проверяет на близость значения
def closeEnough(x, y):
    if abs(x - y) < 0.001:
        return 1
    return 0


def ConjugateGradientMethod(f, x, y,i):
    p1 = -get_diff_f_in_point(x, y, get_diff_f(f(x1, x2), x1))
    p2 = -get_diff_f_in_point(x, y, get_diff_f(f(x1, x2), x2))

    #Вычисляем градиент
    Grad_F_x1 = get_diff_f_in_point(x, y, get_diff_f(f(x1, x2), x1))
    Grad_F_x2 = get_diff_f_in_point(x, y, get_diff_f(f(x1, x2), x2))
    gradSquare = inner_product(p1, p2, p1, p2)

    # используем метод половинного деления для нахождения минимума F1(x + alpha * p)
    alpha = dihotomia(f, 0, 1, x, y, p1, p2)
    # обновляем значения х и y в направлении антиградиента
    x = x + alpha * p1
    y = y + alpha * p2

    newGrad_F_x1 = - Grad_F_x1
    newGrad_F_x2 = - Grad_F_x2
    newGradSquare = inner_product(newGrad_F_x1, newGrad_F_x1, newGrad_F_x1,
                                  newGrad_F_x2)
    # Используем метод Флетчера - Ривса
    beta = newGradSquare / gradSquare
    p1 = newGrad_F_x1 + beta * p1
    p2 = newGrad_F_x2 + beta * p2
    gradSquare = newGradSquare
    print("gradsquare,eps", gradSquare,eps)
    # проверяем условие остановки
    if abs(gradSquare) < eps:
        print([x, y])
        return [x, y, i]
    i = i+1
    print(x, y)
    return ConjugateGradientMethod(f, x, y,i)


def main():
    i = 0
    print("Метод наискорейшего спуска для f1")
    min1 = ConjugateGradientMethod(f1, 0, 0,i)
    print("Метод наискорейшего спуска для f2")
    min2 = ConjugateGradientMethod(f2, -2.048, 2.048,i)
    print("точка минимума f1: ", min1[0:2])
    print("минимум f1: ", f1(min1[0], min1[1]))
    print("количество итерация", min1[2])
    print("точка минимума f2: ", min2[0:2])
    print("минимум f1: ", f2(min2[0], min2[1]))
    print("количество итерация", min1[2])


main()