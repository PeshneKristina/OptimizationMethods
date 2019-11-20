import math

eps = 0.001
phi = (1 + math.sqrt(5)) / 2


# возвращает значение функции
def f(x):
    a = 4
    b = 3
    return a * x + b / (math.exp(x))


# применяем метод золотого сечения
def GoldenRatio(left_point, right_point):
    while True:
        # находим точки с помощью соотношения золотого сечения
        x1 = right_point - (right_point - left_point) / phi
        x2 = left_point + (right_point - left_point) / phi
        print("x1 = {0}, x2 = {1}".format(x1, x2))
        f1 = f(x1)
        f2 = f(x2)
        # сравниваем значение функции в заданных точках
        if f1 >= f2:
            left_point = x1
        else:
            right_point = x2
        print(
            "левый конец интервала: {0} , правый конец интервала: {1}.".format(
                left_point, right_point))
        # проверяем условие остановки
        if closeEnough(right_point, left_point) == 1:
            break
    return average(x1, x2)


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
    min = GoldenRatio(left_point, right_point)
    print("точка минимума", min)
    print("минимум функции",f(min))


main()
