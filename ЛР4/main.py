import numpy as np
import math
import itertools
import matplotlib.pyplot as plt

def step(net):
    if net >= 0:
        return 1
    else:
        return 0

# Считаем net
def net(fi, u):
    return sum(fi[i] * u[i] for i in range(len(u)))

# Вычисляем значение fi
def fi(x, c):
    fi_y = [[np.array(x) - np.array(cc)] for cc in c]
    return [1] + [math.exp(-np.sum(np.power(i, 2))) for i in fi_y]

# Алгоритм обучения
def training_mode(num_of_vec):
    # Запишем центры наших РБФ-нейронов
    c = [[0, 0, 1, 1], [0, 1, 1, 1], [1, 0, 1, 1]]
    u = np.zeros(len(c) + 1)
    etta = 0.3
    errors = np.ones(len(num_of_vec))
    sumError = []

    y = [0]*len(num_of_vec)
    f = [0]*len(num_of_vec)

    era = 0
    out = ''

    while np.sum(errors) != 0:

        for x in range(len(num_of_vec)):
            fi_y = fi(num_of_vec[x], c)
            net_y = net(fi_y, u)
            y[x] = step(net_y)
            f[x] = function_init(num_of_vec[x])
            sigma = f[x] - y[x]

            for i in range(len(u)):
                u[i] += etta * sigma * fi_y[i]

        errors = sum((f[i] ^ y[i]) for i in range(len(num_of_vec)))
        sumError.append(errors)
        out += (f"%d y:{y}, Целевой вектор f:{f}, w:{u} Error = %.d \n" % (era, errors))

        era += 1

        if era >= 1000:
            return -1

    # Проверяем: совпадает ли тестовая функция с целевой
    if test_function(c, u) == initialize():
        print(f"Выборка: {num_of_vec} Функция обучена правильно!\n {out}")
        plt.plot(sumError, 'ro-')
        plt.grid(True)
        plt.show()
        return era
    else:
        print(f"Ошибка при обучении!\n")
        return -1

# Записываем значения для тестовой функции
def test_function(c, u):
    X = ''

    for x in [list(i) for i in itertools.product([0, 1], repeat=4)]:
        fi_y = fi(x, c)
        net_y = net(fi_y, u)
        y = step(net_y)
        X += str(y)

    return X

# Записываем значения для таблицы истинности
def initialize_full():
    n = 4
    X = []
    i = 0
    while i < 2**n:
        x = list(format(i, f'0{n}b'))
        x = [int(s) for s in x]
        X.append(x)
        i += 1

    return X

def initialize():
    X = ''

    for i in [list(i) for i in itertools.product([0, 1], repeat=4)]:
        X += str(function_init(i))

    return X

# Строим нашу целевую функцию с помощью формул
def function_init(x):
    F = int(x[0] or not x[1] or not (x[2] or x[3]))
    return F

if __name__ == "__main__":
    commands = 'Введите команду:' \
    '\n     full        --- обучение нейронной сети и построение графика ошибок для всех векторов' \
    '\n     min         --- обучение нейронной сети и построение графика ошибок для минимального количества векторов' \
    '\n' \
    '\n     exit        --- выход из программы'

    print(commands)

    true = 1
    while true == 1:
        command = input()

        if command == 'full':
            x = initialize_full()
            training_mode(x)
        elif command == 'min':
            num_of_vec = [
                [0, 0, 1, 1],
                [0, 1, 0, 0],
                [0, 1, 0, 1],
                [0, 1, 1, 1],
                [0, 1, 1, 0],
                [1, 0, 0, 0],
                [1, 0, 1, 0],
                [1, 1, 0, 1],
            ]
            training_mode(num_of_vec)
        elif command == 'exit':
            true = 0