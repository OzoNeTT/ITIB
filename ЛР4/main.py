import numpy as np
import math
import itertools
import matplotlib.pyplot as plt

class RBFNeuron:
    def __init__(self, n, x=None):
        self._net = 0
        self._J = 0
        self._fi = None
        self._u = None
        self._n = n
        self._c = None
        self._functionY = None
        self._functionX = x

    def func(self, x):
        return int(x[0] or not x[1] or not (x[2] or x[3]))

    def step(self):
        return 1 if self._net >= 0 else 0

    def net(self):
        self._net = sum(self._fi[i] * self._u[i] for i in range(len(self._u)))

    def j_count(self):
        self._J = min(self._functionY.count(1), self._functionY.count(0))
        c = []
        for i in range(len(self._functionY)):
            if self._functionY.count(1) < self._functionY.count(0):
                if self._functionY[i] == 1:
                    c.append(self._functionX[i])
            else:
                if self._functionY[i] == 0:
                    c.append(self._functionX[i])

        self._c = c.copy()

    def initialize(self):
        if self._functionX is None:
            X = []
            Y = []
            for i in range(16):
                x = [math.floor(i // 8) % 2, math.floor(i // 4) % 2, math.floor(i // 2) % 2, math.floor(i // 1) % 2]
                X.append(x)
                Y.append(self.func(x))
            self._functionX = X.copy()
            self._functionY = Y.copy()
        else:
            Y = []
            for i in range(len(self._functionX)):
                Y.append(self.func(self._functionX[i]))

    def fi(self, x, c):
        fi_y = [[np.array(x) - np.array(cc)] for cc in c]
        return [1] + [math.exp(-np.sum(np.power(i, 2))) for i in fi_y]

    def study(self):
        self.initialize()
        self.j_count()
        self._u = np.zeros(len(self._c) + 1)

        errors = np.ones(len(self._functionX))
        sumError = []

        y = [0] * len(self._functionX)
        f = [0] * len(self._functionX)

        era = 0
        out = ''

        while np.sum(errors) != 0:

            for x in range(len(self._functionX)):
                self._fi = self.fi(self._functionX[x], self._c)
                self.net()
                y[x] = self.step()
                f[x] = self._functionY[x]
                sigma = f[x] - y[x]

                for i in range(len(self._u)):
                    self._u[i] += self._n * sigma * self._fi[i]

            errors = sum((f[i] ^ y[i]) for i in range(len(self._functionX)))
            sumError.append(errors)
            out += (f"%d y:{y}, Целевой вектор f:{f}, w:{self._u} Error = %.d \n" % (era, errors))

            era += 1

            if era >= 1000:
                return -1


        print(f"Выборка: {self._functionX} Функция обучена правильно!\n {out}")
        plt.plot(sumError, 'ro-')
        plt.grid(True)
        plt.show()
        return era



def main():
    obj = RBFNeuron(0.3)
    obj.study()

if __name__ == '__main__':
    main()
