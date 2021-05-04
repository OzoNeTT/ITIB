import math

class BPNNetwork:
    def __init__(self, input_vector, target, N, J, M, lr):
        self.input = input_vector
        self.target = target
        self.N = N
        self.J = J
        self.M = M
        self.lr = lr
        self.hw = [[0] * (N + 1) for _ in range(J)]
        self.ow = [[0] * (J + 1) for _ in range(M)]

    def hidden_net(self, idx):
        net = self.hw[idx][0]
        for i in range(self.N):
            net += self.hw[idx][i + 1] * self.input[i]
        return net

    def output_net(self, idx, in_out_vector):
        net = self.ow[idx][0]
        for i in range(self.J):
            net += self.ow[idx][i + 1] * in_out_vector[i]
        return net

    def f(self, net):
        return (1 - math.exp((-1) * net))/(1 + math.exp((-1) * net))

    def df(self, net) -> float:
        return 0.5 * (1 - (self.f(net) ** 2))

    def epsilon(self, y):
        eps = 0
        for i in range(len(self.target)):
            eps += (self.target[i] - y[i]) ** 2
        return math.sqrt(eps)

    def get_sum(self, idx, list_delta):
        res = 0
        for i in range(len(list_delta)):
            res += self.ow[i][idx] * list_delta[i]
        return res

    def study(self):
        epsilon = 1
        K = 0
        while epsilon > 0.0001:
            # --- ШАГ 1

            # Все веса скрытого слоя
            all_net_hl = []
            # Все веса выходного слоя
            all_net_ol = []

            input_in_out_layer = [0] * (self.J + 1)
            out = []

            for i in range (self.J):
                net_hidden = self.hidden_net(i)
                all_net_hl.append(net_hidden)
                input_in_out_layer[i] = self.f(net_hidden)

            for i in range(self.M):
                net_out = self.output_net(i, input_in_out_layer)
                all_net_ol.append(net_out)
                out.append(self.f(net_out))

            #---ШАГ 2

            all_out_error = []
            all_hidden_error = []

            for i in range(len(all_net_ol)):
                df = self.df(all_net_ol[i])
                delta = df * (self.target[i] - out[i])
                all_out_error.append(delta)

            for i in range(len(all_net_hl)):
                df = self.df(all_net_hl[i])
                delta = df * self.get_sum(i, all_out_error)
                all_hidden_error.append(delta)

            #---ШАГ 3

            for J in range(self.J):
                self.hw[J][0] += self.lr * all_hidden_error[J]
                for N in range(self.N):
                    self.hw[J][N + 1] += self.lr * self.input[N] * all_hidden_error[J]

            for M in range(self.M):
                self.ow[M][0] += self.lr * all_out_error[M]
                for J in range(self.J):
                    self.ow[M][J + 1] += self.lr * input_in_out_layer[J] * all_out_error[M]

            K += 1
            epsilon = self.epsilon(out)
            #print(f"hidden_weights = {self.hw}")
            #print(f"output_layer = {self.ow}")
            result = [round(x, 3) for x in out]
            print(f"Result: {result},\t E({K}): {epsilon}")
            if result == self.target:
                break

if __name__ == '__main__':
    n = BPNNetwork([2, 1], [0.2, 0.1], 2, 1, 2, 0.5)
    n.study()