import numpy as np
import math
import matplotlib.pyplot as plt

FUNCTION = [True, True, True, True, True, False, False, False, True, True, True, True, True, True, True, True]
SELECTED = [
    [1, 0, 0, 0, 1],
    [1, 0, 1, 1, 1],
    [1, 1, 0, 1, 0],
    [1, 1, 0, 1, 1],
    [1, 1, 1, 1, 0]
]
SELECTED_FUNC = [True, True, False, True, True]

def function_one(net):
    return 1 if net >= 0 else 0

def function_two_dxdy(net):
    return 1 / (np.cosh(2 * net) + 1)

def function_two(net):
    return 0.5 * (np.tanh(net) + 1)


def net_calculator(weights, x):
    return weights[0] + weights[1] * x[1] + weights[2] * x[2] + weights[3] * x[3] + weights[4] * x[4]

def weights_correction(weights, sigma, n, x, dfdnet):
    new_weights = []
    for i in range(5):
        new_weights.append(weights[i] + n * sigma * dfdnet * x[i])
    return  new_weights

def predict_y(weights, type):
    predicted_y = []
    for i in range(16):
        x = [1, math.floor(i // 8) % 2, math.floor(i // 4) % 2, math.floor(i // 2) % 2, math.floor(i // 1) % 2]
        if type == 1:
            predicted_y.append(True if function_one(net_calculator(weights, x)) == 1 else False)
        elif type == 2:
            predicted_y.append(True if function_two(net_calculator(weights, x)) >= 0.5 else False)
    return predicted_y

def exception_counter(predicted_y):
    ex = 0
    for i in range(16):
        if predicted_y[i] is not FUNCTION[i]:
            ex += 1
    return ex

def exception_counter_selected(predicted_y):
    ex = 0
    for i in range(5):
        if predicted_y[i] is not SELECTED_FUNC[i]:
            ex += 1
    return ex

def study1(type, nt):
    print("EPOCH".rjust(5), "FUNCTION".rjust(18), "WEIGHTS".rjust(39), "E".rjust(3))
    print("_" * 5, " ", "_" * 16, "_" * 39, " __")
    weights = [0, 0, 0, 0, 0]
    errors = []
    epoch = 0
    n = nt
    while True:
        y = predict_y(weights, type)
        ex = exception_counter(y)
        errors.append([epoch, ex])
        y_string = ''.join(['1' if it else '0' for it in y])
        w_string = ', '.join([str("%.3f" % it) if it < 0 else str("%.4f" % it) for it in weights])

        print(str(epoch).rjust(5), str(y_string).rjust(18), str(w_string).rjust(39), str(ex).rjust(3))
        if ex == 0:
            break

        for i in range(16):
            x = [1, math.floor(i // 8) % 2, math.floor(i // 4) % 2, math.floor(i // 2) % 2, math.floor(i // 1) % 2]
            dfdnet = 1

            tn = int(FUNCTION[i])
            yn = int(y[i])
            sigm = tn - yn
            net = net_calculator(weights, x)
            if type == 2:
                dfdnet = function_two_dxdy(net)

            weights = weights_correction(weights, sigm, n, x, dfdnet)

        epoch += 1
    return errors

def study2(type, nt):
    print("EPOCH".rjust(5), "FUNCTION".rjust(18), "WEIGHTS".rjust(39), "E".rjust(3))
    print("_" * 5, " ", "_" * 16, "_" * 39, " __")
    weights = [0, 0, 0, 0, 0]
    errors = []
    epoch = 0
    n = nt
    while True:
        y = predict_y(weights, type)
        ex = exception_counter_selected(y)
        errors.append([epoch, ex])
        y_string = ''.join(['1' if it else '0' for it in y])
        w_string = ', '.join([str("%.3f" % it) if it < 0 else str("%.4f" % it) for it in weights])

        print(str(epoch).rjust(5), str(y_string).rjust(18), str(w_string).rjust(39), str(ex).rjust(3))
        if ex == 0:
            break

        for i in range(5):
            x = SELECTED[i]
            dfdnet = 1

            tn = int(SELECTED_FUNC[i])
            yn = int(y[i])
            sigm = tn - yn
            net = net_calculator(weights, x)
            if type == 2:
                dfdnet = function_two_dxdy(net)

            weights = weights_correction(weights, sigm, n, x, dfdnet)

        epoch += 1
    return errors

def printgraph(err):
    x, y = err.T
    plt.ylabel('E')
    plt.xlabel('epoch')
    plt.scatter(x, y)
    plt.plot(x, y)
    plt.show()

def main():
    print('-' * 30, 'FA 1st type', '-' * 30)
    print()
    err1 = np.array(study1(1, 0.8))
    print()
    print()
    print('-' * 30, 'FA 2nd type', '-' * 30)
    print()
    err2 = np.array(study1(2, 0.3))
    print()
    print()
    print('-' * 30, 'FA 2nd type', '-' * 30)
    print()
    err3 = np.array(study2(2, 0.3))
    print()
    print()

    printgraph(err1)
    printgraph(err2)
    printgraph(err3)


if __name__ == '__main__':
    main()