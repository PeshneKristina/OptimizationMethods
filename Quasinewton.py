from sympy import *
import math

eps = 0.015
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


# возвращает норму двух векторов
def get_norm(x, y):
    return math.sqrt(x ** 2 + y ** 2)


# вспомогательная функция для выбора направления спуска методом дихотомии
def helper_function(f, x, y, alpha):
    return f(x - alpha * get_diff_f_in_point(x, y, get_diff_f(f(x1, x2), x1)),
             y - alpha * get_diff_f_in_point(x, y, get_diff_f(f(x1, x2), x2)))


# метод дихотомии
# метод половинного деления для нахождения минимума минимума F1(x + alpha * p)
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
    if abs(x - y) < 0.01:
        return 1
    return 0


def Quasinewton(f, x0, y0):
    # Вводим единичную матрицу
    i = 0
    I = [[1, 0], [0, 1]]
    H = I
    x = x0
    y = y0
    Grad_F_x1 = get_diff_f_in_point(x, y, get_diff_f(f(x1, x2), x1))
    Grad_F_x2 = get_diff_f_in_point(x, y, get_diff_f(f(x1, x2), x2))

    # Проверка на окончание поиска
    while get_norm(Grad_F_x1, Grad_F_x2) > eps:
        x0 = x
        y0 = y
        # Находим точку в направлении которой будем производить поиск
        s0 = -(H[0][0] * Grad_F_x1 + H[0][1] * Grad_F_x2)
        s1 = -(H[1][0] * Grad_F_x1 + H[1][1] * Grad_F_x2)
        # используем метод половинного деления для нахождения минимума F1(x + alpha * p)
        alpha = dihotomia(f, 0, 1000, x, y)
        x = x0 + alpha * s0
        y = y0 + alpha * s1

        # Вычисляем шаг алгоритма
        dx = x - x0
        dy = y - y0

        Grad_F_x1 = get_diff_f_in_point(x, y, get_diff_f(f(x1, x2), x1))
        Grad_F_x2 = get_diff_f_in_point(x, y, get_diff_f(f(x1, x2), x2))
        Grad_F_x0 = get_diff_f_in_point(x0, y0, get_diff_f(f(x1, x2), x1))
        Grad_F_y0 = get_diff_f_in_point(x0, y0, get_diff_f(f(x1, x2), x2))

        # Вычисляем изменение градиента
        g0 = Grad_F_x1 - Grad_F_x0
        g1 = Grad_F_x2 - Grad_F_y0

        # Находим приближение гессиана
        b = []
        b.append([g0 * g0 * I[0][0] + g0 * g1 * I[0][1],
                  g0 * g1 * I[0][0] + g1 * g1 * I[0][1]])
        b.append([g0 * g0 * I[1][0] + g0 * g1 * I[1][1],
                  g0 * g1 * I[1][0] + g1 * g1 * I[1][1]])

        qwe = abs(dx * g0 + dy * g1)

        ax = I

        asd = ((g0 * I[0][0] + g1 * I[1][0]) * g0 + (
                g0 * I[0][1] + g1 * I[1][1]) * g1)

        ac = []
        ac.append([1 / qwe * (dx * dx) - 1 / asd * (
                b[0][0] * I[0][0] + b[0][1] * I[1][0]),
                   1 / qwe * (dx * dy) - 1 / asd * (
                           b[0][0] * I[1][0] + b[0][1] * I[1][1])])
        ac.append([1 / qwe * (dx * dy) - 1 / asd * (
                b[1][0] * I[0][0] + b[1][1] * I[1][0]),
                   1 / qwe * (dy * dy) - 1 / asd * (
                           b[1][0] * I[1][0] + b[1][1] * I[1][1])])

        H[0][0] = ax[0][0] + ac[0][0]
        H[0][1] = ax[0][1] + ac[0][1]
        H[1][0] = ax[1][0] + ac[1][0]
        H[1][1] = ax[1][1] + ac[1][1]

        print("x y",[x, y])
        #print("1", Grad_F_x1)
        #print("2", Grad_F_x2)
        i=i+1
        print(get_norm(Grad_F_x1, Grad_F_x2), eps)

    # print(x, y)
    return [x, y,i]


def main():
    print("Метод наискорейшего спуска для f1")
    min1 = Quasinewton(f1, 0.389, 0.5)
    print("Метод наискорейшего спуска для f2")
    min2 = Quasinewton(f2, -2.4, 2.4)
    print("точка минимума f1: ", min1[0:2])
    print("минимум f1: ", f1(min1[0], min1[1]))
    print("количество итерация", min1[2])
    print("точка минимума f2: ", min2[0:2])
    print("минимум f1: ", f2(min2[0], min2[1]))
    print("количество итерация", min1[2])

main()
