import numpy

# эта библиотека позволяет работать с массивами как с векторами

alpha = 1
beta = 0.5
gamma = 2


# возвращает значение функции
def f1(x1, x2):
    return 100 * (x2 - x1 ** 2) ** 2 + 5 * (1 - x1) ** 2


# возвращает значение функции
def f2(x1, x2):
    return (x1 ** 2 + x2 - 11) ** 2 + (x1 + x2 ** 2 - 7) ** 2


# применяем метод деформируемого многогранника
def Nelder_mead(f):
    v1 = numpy.array([0, 0])
    v2 = numpy.array([1, 0])
    v3 = numpy.array([0, 1])

    side1 = numpy.linalg.norm(v1 - v2, ord=2)
    side2 = numpy.linalg.norm(v1 - v3, ord=2)
    side3 = numpy.linalg.norm(v2 - v3, ord=2)
    p = (side1 + side2 + side3) / 2
    s = numpy.math.sqrt(p * (p - side1) * (p - side2) * (p - side3))

    while not (s < 0.000001):
        # создаем массив из значений функции в заданных точках
        vector_array = {tuple(v1): f(v1[0], v1[1]),
                        tuple(v2): f(v2[0], v2[1]),
                        tuple(v3): f(v3[0], v3[1])}
        print(vector_array)
        # сортируем массив, чтобы найти вектор, в которой функция минимальна
        sort_vector_array = sorted(vector_array.items(), key=lambda x: x[1])
        print(sort_vector_array)

        b = numpy.array(sort_vector_array[0][0])
        g = numpy.array(sort_vector_array[1][0])
        w = numpy.array(sort_vector_array[2][0])

        print("best = ", b)
        print("good = ", g)
        print("worst = ", w)

        # определяем среднее значение между точками лучшего и среднего вариантов
        mid = (g + b) / 2
        # print("mid = ", mid)

        # отражение
        # отражаем точку w относительно mid
        xr = mid + alpha * (mid - w)
        # print("xr = ", xr)

        if f(xr[0], xr[1]) < f(g[0], g[1]):
            w = xr
        else:
            if f(xr[0], xr[1]) < f(w[0], w[1]):
                w = xr
            c = (w + mid) / 2
            if f(c[0], c[1]) < f(w[0], w[1]):
                w = c

        if f(xr[0], xr[1]) < f(b[0], b[1]):
            # растяжение
            # найдя хорошую точку, пробуем увеличить расстояние,
            # чтобы найти вариант лучше
            xe = mid + gamma * (xr - mid)
            # print("xe = ", xe)
            if f(xe[0], xe[1]) < f(xr[0], xr[1]):
                w = xe
            else:
                w = xr

        if f(xr[0], xr[1]) > f(g[0], g[1]):
            # сжатие
            # используем метод сжатия, если нам не повезло и мы не нашли хороших точек
            # ищем хорошие точки внутри треугольника
            xc = mid + beta * (w - mid)
            # print("xc = ", xc)
            if f(xc[0], xc[1]) < f(w[0], w[1]):
                w = xc

        # обновление точек
        v1 = w
        v2 = g
        v3 = b
        side1 = numpy.linalg.norm(v1 - v2, ord=2)
        side2 = numpy.linalg.norm(v1 - v3, ord=2)
        side3 = numpy.linalg.norm(v2 - v3, ord=2)
        p = (side1 + side2 + side3) / 2
        s = numpy.math.sqrt(p * (p - side1) * (p - side2) * (p - side3))
    return b


def main():
    print("-------метод деформируемого многогранника для f1-------")
    min1 = Nelder_mead(f1)
    print("-------метод деформируемого многогранника для f2-------")
    min2 = Nelder_mead(f2)
    print("точка минимумв f1 = ", min1)
    print("минимум f1 = ", f1(min1[0], min1[1]))
    print("точка минимумв f2 = ", min2)
    print("минимум f2 = ", f2(min1[0], min1[1]))


main()
