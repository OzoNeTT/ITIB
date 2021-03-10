import numpy as np
import math
import matplotlib.pyplot as plt


class Neuron(object):
    def __init__(self, M, a, b, eta):
        self._M = M
        self._a = a
        self._b = b
        self._eta = eta

        self._learnFunction = []  
        self._mainFunction = [] 

        self._N = 20

        self._windowSize = abs(self._a) + abs(self._b)
        self._w = np.zeros(self._windowSize + 1)

        self._epsilon = 1
        self._delta = 0
        self._k = 0

        self._era = []
        self._error = []

    def net(self, windowSize, x, w):
        net = (sum(w[i + 1] * x[i] for i in range(windowSize)))
        return net

    def getX(self, a, b):
        vectorX = []

        dx = (b - a) / self._N

        for i in range(self._N):
            vectorX.append(a + i * dx)

        return vectorX

    def getY(self, a, b):
        vectorY = []
        vectorX = self.getX(a, b)

        for i in range(self._N):
            vectorY.append(math.exp(vectorX[i] - 1))

        return vectorY

    def training_mode(self):
        self._learnFunction = [0] * self._N
        self._mainFunction = self.getY(self._a, self._b)

        self._w = np.zeros(self._windowSize + 1)

        while self._k < self._M:
            for q in range(self._windowSize):
                self._learnFunction[q] = self._mainFunction[q]

            for i in range(self._windowSize, self._N):
                self._learnFunction[i] = self.net(self._windowSize, self._mainFunction[i - self._windowSize: i],
                                                  self._w)
                self._delta = self._mainFunction[i] - self._learnFunction[i]

                for j in range(self._windowSize):
                    self._w[j + 1] += self._eta * self._delta * self._mainFunction[i - self._windowSize + j]

            self._epsilon = sum(
                (self._mainFunction[index] - self._learnFunction[index]) ** 2 for index in range(self._N))
            self._epsilon = math.sqrt(self._epsilon)

            self._era.append(self._k)
            self._error.append(self._epsilon)

            self._k += 1


    def test_func(self):
        vecFX = self.getX(self._a, self._b)
        vecFT = self.getY(self._a, self._b)
        vectorX = self.getX(self._b, 2 * self._b - self._a)
        vectorY = self.getY(self._b, 2 * self._b - self._a)

        testFunction = [0] * 24
        TF = [0] * self._N

        for i in range(self._N - self._windowSize, self._N):
            testFunction[i - (self._N - self._windowSize)] = self._learnFunction[i]

        for j in range(self._windowSize, len(vectorY) + self._windowSize):
            vectorTestFunction = [0] * self._windowSize
            for k in range(self._windowSize):
                vectorTestFunction[k] = testFunction[k + j - self._windowSize]
            testFunction[j] = self.net(self._windowSize, vectorTestFunction, self._w)

        for i in range(self._windowSize, len(testFunction)):
            TF[i - self._windowSize] = testFunction[i]

        plt.plot(vecFX, vecFT, 'go-')
        plt.plot(vectorX, vectorY, 'bo-')
        plt.plot(vectorX, TF, 'ro')

        plt.grid(True)
        plt.show()



if __name__ == '__main__':
    obj = Neuron(10, -2, 2, 0.01)
    obj.training_mode()
    obj.test_func()

    obj = Neuron(1000, -2, 2, 0.01)
    obj.training_mode()
    obj.test_func()