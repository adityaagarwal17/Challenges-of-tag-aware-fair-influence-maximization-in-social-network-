import math
import random


class IMM:
    l0 = 1

    def __init__(self, G: any, is_directed: bool, num_nodes: int, size: int, eps: float):
        random.seed(0)
        self.G = G
        self.is_directed = is_directed
        self.n = num_nodes
        self.k = size
        self.eps = eps

    def sampling(self, li: float) -> (list, list):
        S = []
        R = []
        LB = 1
        eps_p = self.eps * math.sqrt(2)
        for i in range(1, int(math.log2(self.n - 1)) + 1):
            x = self.n / (math.pow(2, i))
            lambda_p = ((2 + 2 * eps_p / 3) * (self.log_cnk() + li * math.log(self.n) + math.log(math.log2(self.n)))
                        * self.n) / pow(eps_p, 2)
            theta = lambda_p / x
            while len(R) <= theta:
                v = random.randint(0, self.n - 1)
                rr = self.generate_rr(v)
                S.append(v)
                R.append(rr)
            Si, f = self.node_selection(R)
            if self.n * f >= (1 + eps_p) * x:
                LB = self.n * f / (1 + eps_p)
                break
        alpha = math.sqrt(li * math.log(self.n) + math.log(2))
        beta = math.sqrt((1 - 1 / math.e) * (self.log_cnk() + li * math.log(self.n) + math.log(2)))
        lambda_aster = 2 * self.n * pow(((1 - 1 / math.e) * alpha + beta), 2) * pow(self.eps, -2)
        theta = lambda_aster / LB
        while len(R) <= theta:
            v = random.randint(0, self.n - 1)
            rr = self.generate_rr(v)
            S.append(v)
            R.append(rr)
        return S, R

    def log_cnk(self) -> float:
        res = 0
        for i in range(self.n - self.k + 1, self.n + 1):
            res += math.log(i)
        for i in range(1, self.k + 1):
            res -= math.log(i)
        return res

    def node_selection(self, R: list) -> (set, float):
        S = set()
        rr_profit = [0 for _ in range(self.n + 1)]
        node_rr_set = dict()
        cover_count = 0
        for j in range(len(R)):
            rr = R[j]
            for rr_node in rr:
                rr_profit[rr_node] += 1
                if rr_node not in node_rr_set:
                    node_rr_set[rr_node] = set()
                node_rr_set[rr_node].add(j)
        while len(S) < self.k:
            max_profit = max(rr_profit)
            if max_profit > 0:
                max_node = rr_profit.index(max_profit)
            else:
                break
            S.add(max_node)
            cover_count += len(node_rr_set[max_node])
            index_set = []
            index_set.extend(node_rr_set[max_node])
            for jj in index_set:
                rr = R[jj]
                for rr_node in rr:
                    rr_profit[rr_node] -= 1
                    node_rr_set[rr_node].remove(jj)
        return S, cover_count / len(R)

    def generate_rr(self, node: int) -> set:
        active_set = list()
        active_set.append(node)
        active_nodes = set()
        active_nodes.add(node)
        while len(active_set) > 0:
            new_active_set = list()
            for v in active_set:
                for u, _, data in self.G.in_edges(nbunch=v, data=True):
                    if u not in active_nodes:
                        if random.random() < data['weight']:
                            active_nodes.add(u)
                            new_active_set.append(u)
            active_set = new_active_set
        return active_nodes

    def run(self) -> (list, list):
        li = self.l0 * (1 + math.log(2) / math.log(self.n))
        S, R = self.sampling(li)
        return S, R
