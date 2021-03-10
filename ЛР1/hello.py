import numpy as np
import math
import matplotlib.pyplot as plt


class NeuralNetwork:
    def __init__(self, type, n, func):
        self.__type = type
        self.__n = n
        self.__net = 0
        self.__weights = [0, 0, 0, 0, 0]
        self.__func = func
        self.__errors = []

    def function_one(self):
        return 1 if self.__net >= 0 else 0

    def function_two(self):
        return 0.5 * (np.tanh(self.__net) + 1)

    def function_two_dxdy(self):
        return 1 / (np.cosh(2 * self.__net) + 1)

    def net_calculator(self, x):
        self.__net =  self.__weights[0] + self.__weights[1] * x[1] + self.__weights[2] * x[2] + self.__weights[3] * x[3] + self.__weights[4] * x[4]

    def weights_correction(self, sigma, x, dfdnet):
        for i in range(5):
            self.__weights[i] = self.__weights[i] + self.__n * sigma * dfdnet * x[i]

    def study(self):
        print("EPOCH".rjust(5), "FUNCTION".rjust(18), "WEIGHTS".rjust(39), "E".rjust(3))
        print("_" * 5, " ", "_" * 16, "_" * 39, " __")
        epoch = 0
        while True:
            error = 0
            predicted_y = False
            y = ""
            for i in range(16):
                x = [1, math.floor(i // 8) % 2, math.floor(i // 4) % 2, math.floor(i // 2) % 2, math.floor(i // 1) % 2]
                if self.__type == 1:
                    self.net_calculator(x)
                    predicted_y = True if self.function_one() == 1 else False
                elif self.__type == 2:
                    self.net_calculator(x)
                    predicted_y = True if self.function_two() >= 0.5 else False
                if predicted_y is not self.__func[i]:
                    error += 1
                y += str(int(predicted_y))
                dfdnet = 1
                tn = int(self.__func[i])
                yn = int(predicted_y)
                sigm = tn - yn
                self.net_calculator(x)
                if self.__type == 2:
                    dfdnet = self.function_two_dxdy()
                self.weights_correction(sigm, x, dfdnet)
            w_string = ', '.join([str("%.3f" % it) if it < 0 else str("%.4f" % it) for it in self.__weights])
            self.__errors.append([epoch, error])
            print(str(epoch).rjust(5), str(y).rjust(18), str(w_string).rjust(39), str(error).rjust(3))
            if error == 0:
                break
            epoch += 1

    def study_selected(self):
        SELECTED = [
            [1, 0, 0, 1, 1],
            [1, 0, 1, 0, 0],
            [1, 0, 1, 0, 1],
            [1, 0, 1, 1, 1],
            [1, 0, 1, 1, 0],
            [1, 1, 0, 0, 0],
            [1, 1, 0, 1, 0],
            [1, 1, 1, 0, 1],
        ]
        SELECTED_FUNC = [ True,True, False, False, False, True, True, True]
        print("EPOCH".rjust(5), "FUNCTION".rjust(18), "WEIGHTS".rjust(39), "E".rjust(3))
        print("_" * 5, " ", "_" * 16, "_" * 39, " __")
        epoch = 0
        while True:
            error = 0
            predicted_y = False
            y = ""
            for i in range(len(SELECTED)):
                if self.__type == 1:
                    self.net_calculator(SELECTED[i])
                    predicted_y = True if self.function_one() == 1 else False
                elif self.__type == 2:
                    self.net_calculator(SELECTED[i])
                    predicted_y = True if self.function_two() >= 0.5 else False
                if predicted_y is not SELECTED_FUNC[i]:
                    error += 1
                y += str(int(predicted_y))
                dfdnet = 1
                tn = int(SELECTED_FUNC[i])
                yn = int(predicted_y)
                sigm = tn - yn
                self.net_calculator(SELECTED[i])
                if self.__type == 2:
                    dfdnet = self.function_two_dxdy()
                self.weights_correction(sigm, SELECTED[i], dfdnet)
            w_string = ', '.join([str("%.3f" % it) if it < 0 else str("%.4f" % it) for it in self.__weights])
            self.__errors.append([epoch, error])
            print(str(epoch).rjust(5), str(y).rjust(18), str(w_string).rjust(39), str(error).rjust(3))
            if error == 0:
                break
            epoch += 1

        predicted = []
        for i in range(16):
            x = [1, math.floor(i // 8) % 2, math.floor(i // 4) % 2, math.floor(i // 2) % 2, math.floor(i // 1) % 2]
            if self.__type == 1:
                self.net_calculator(x)
                predicted.append(True if self.function_one() == 1 else False)
            elif self.__type == 2:
                self.net_calculator(x)
                predicted.append(True if self.function_two() >= 0.5 else False)
        y_string = ''.join(['1' if it else '0' for it in predicted])
        print(y_string)

    def printgraph(self):
        err = np.array(self.__errors)
        x, y = err.T
        plt.ylabel('E')
        plt.xlabel('epoch')
        plt.scatter(x, y)
        plt.plot(x, y)
        plt.show()

    def reset(self, type, n, func):
        self.__type = type
        self.__n = n
        self.__net = 0
        self.__weights = [0, 0, 0, 0, 0]
        self.__func = func
        self.__errors = []

def main():
    FUNCTION = [True, True, True, True, True, False, False, False, True, True, True, True, True, True, True, True]
    nw = NeuralNetwork(1, 0.3, FUNCTION)
    print('-' * 30, 'FA 1st type', '-' * 30)
    print()
    nw.study()
    nw.printgraph()
    print()
    print()
    print('-' * 30, 'FA 2nd type', '-' * 30)
    print()
    nw.reset(2, 0.3, FUNCTION)
    nw.study()
    nw.printgraph()
    print()
    print()
    print('-' * 30, 'FA 2nd type', '-' * 30)
    print()
    nw.reset(2, 0.3, FUNCTION)
    nw.study_selected()
    nw.printgraph()
    print()
    print()


if __name__ == '__main__':
    main()
