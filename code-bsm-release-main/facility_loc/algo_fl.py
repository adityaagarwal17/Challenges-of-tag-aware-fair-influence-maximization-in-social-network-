import functools
import math
import timeit
from queue import PriorityQueue


@functools.total_ordering
class QItem:
    def __init__(self, item_id: int, gain: float, iteration: int):
        self.item_id = item_id
        self.gain = gain
        self.iteration = iteration

    def __lt__(self, obj):
        return self.gain > obj.gain

    def __eq__(self, obj):
        return self.gain == obj.gain

    def __ne__(self, obj):
        return self.gain != obj.gain

    def __gt__(self, obj):
        return self.gain < obj.gain


def calc_obj_vals(bmat, sol, list_attr, list_groups):
    m = len(bmat[0])
    bvec = [0.0] * m
    for v in sol:
        for u in range(m):
            bvec[u] = max(bvec[u], bmat[v][u])
    val_f = sum(bvec) / len(list_attr)
    vals_g = []
    m = len(bvec)
    c = len(list_groups)
    for j in range(c):
        vals_g.append(0)
    for u in range(m):
        j = list_attr[u]
        vals_g[j] += bvec[u]
    for j in range(c):
        vals_g[j] /= len(list_groups[j])
    val_g = min(vals_g)
    return val_f, val_g, vals_g


def read_items(input_path: str):
    list_items = []
    with open(input_path, 'r') as input_file:
        line_no = 0
        for line in input_file:
            tokens = line.strip().split(' ')
            if line_no == 0:
                n = int(tokens[0])
                for i in range(n):
                    list_items.append(list())
            else:
                item_id = int(tokens[0])
                for i in range(1, len(tokens)):
                    list_items[item_id].append(float(tokens[i]))
            line_no += 1
    return list_items


def read_users(input_path: str):
    list_users = []
    with open(input_path, 'r') as input_file:
        line_no = 0
        for line in input_file:
            tokens = line.strip().split(' ')
            if line_no == 0:
                m = int(tokens[0])
                for i in range(m):
                    list_users.append(list())
            else:
                user_id = int(tokens[0])
                for i in range(1, len(tokens)):
                    list_users[user_id].append(float(tokens[i]))
            line_no += 1
    return list_users


def dist2(a: list, b: list):
    if len(a) != len(b):
        print("Error: dimension not match")
    distance2 = 0
    for i in range(len(a)):
        distance2 += (a[i] - b[i]) * (a[i] - b[i])
    return distance2


def generate_benefit_mat(list_items: list, list_users: list):
    n = len(list_items)
    m = len(list_users)
    mat = [[0.0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            b_ij = math.exp(- dist2(list_items[i], list_users[j]))
            if b_ij > 1e-3:
                mat[i][j] = b_ij
    return mat


def read_attr(input_path: str):
    list_attr = []
    list_group = []
    with open(input_path, 'r') as input_file:
        line_no = 0
        for line in input_file:
            tokens = line.strip().split(' ')
            if line_no == 0:
                m = int(tokens[0])
                c = int(tokens[1])
                for i in range(m):
                    list_attr.append(-1)
                for j in range(c):
                    list_group.append(set())
            else:
                i = int(tokens[0])
                j = int(tokens[1])
                list_attr[i] = j
                list_group[j].add(i)
            line_no += 1
    return list_attr, list_group


def greedy_fl(bmat: list[list[float]], k: int):
    start = timeit.default_timer()
    n = len(bmat)
    m = len(bmat[0])
    sol = list()
    bvec = [0.0] * m
    q = PriorityQueue()

    max_id = -1
    max_gain = 0
    for v in range(n):
        gain = 0
        for u in range(m):
            gain += bmat[v][u]
        q.put(QItem(v, gain, 0))
        if gain > max_gain:
            max_id = v
            max_gain = gain
    sol.append(max_id)
    for u in range(m):
        bvec[u] = max(bvec[u], bmat[max_id][u])

    for it in range(1, k):
        max_id = -1
        while not q.empty():
            q_item = q.get()
            if q_item.item_id not in sol and q_item.iteration < it:
                gain = 0
                for u in range(m):
                    if bvec[u] < bmat[q_item.item_id][u]:
                        gain += (bmat[q_item.item_id][u] - bvec[u])
                if gain > 0:
                    q.put(QItem(q_item.item_id, gain, it))
            elif q_item.item_id not in sol:
                max_id = q_item.item_id
                break
        if max_id >= 0:
            sol.append(max_id)
            for u in range(m):
                bvec[u] = max(bvec[u], bmat[max_id][u])
        else:
            break
    stop = timeit.default_timer()
    return sol, (stop - start)


def saturate_fl(bmat: list[list[float]], k: int, attr: list[int], groups: list[set]):
    start = timeit.default_timer()
    sol_best = list()
    c = len(groups)
    n = len(bmat)
    m = len(bmat[0])
    eps = 0.05
    mc = [len(groups[j]) for j in range(c)]

    g_min = 0
    g_max = 1
    while g_min < (1 - eps) * g_max:
        g_cur = (g_min + g_max) / 2
        caps = [max(1.0, math.floor(g_cur * mc[j])) for j in range(c)]

        sol = list()
        bvec = [0.0] * m
        q = PriorityQueue()

        max_id = -1
        max_gain = 0
        for v in range(n):
            gains = [0.0] * c
            for u in range(m):
                gains[attr[u]] += bmat[v][u]
            gain = sum([min(caps[j], gains[j]) for j in range(c)])
            if gain > 0:
                q.put(QItem(v, gain, 0))
            if gain > max_gain:
                max_id = v
                max_gain = gain
        sol.append(max_id)
        bgroups = [0.0] * c
        for u in range(m):
            bvec[u] = max(bvec[u], bmat[max_id][u])
            bgroups[attr[u]] += bvec[u]

        for it in range(1, k):
            max_id = -1
            while not q.empty():
                q_item = q.get()
                if q_item.item_id not in sol and q_item.iteration < it:
                    gains = [0.0] * c
                    for u in range(m):
                        if bvec[u] < bmat[q_item.item_id][u]:
                            gains[attr[u]] += (bmat[q_item.item_id][u] - bvec[u])
                    gain = 0.0
                    for j in range(c):
                        gain += min(gains[j], max(0.0, caps[j] - bgroups[j]))
                    if gain > 0:
                        q.put(QItem(q_item.item_id, gain, it))
                elif q_item.item_id not in sol:
                    max_id = q_item.item_id
                    break
            if max_id >= 0:
                sol.append(max_id)
                bgroups = [0.0] * c
                for u in range(m):
                    bvec[u] = max(bvec[u], bmat[max_id][u])
                    bgroups[attr[u]] += bvec[u]
            else:
                break
        is_covered = True
        for j in range(c):
            if bgroups[j] < caps[j]:
                is_covered = False
                break
        if is_covered:
            g_min = g_cur
            sol_best = list(sol)
        else:
            g_max = g_cur
    stop = timeit.default_timer()
    return sol_best, (stop - start)


def smsc_fl(bmat: list[list[float]], k: int, beta: float, attr: list[int], groups: list[set]):
    start = timeit.default_timer()
    n = len(bmat)
    m = len(bmat[0])
    sol_best = list()
    eps = 1 / math.e
    if len(groups) > 2:
        return None

    sol_f = list()
    bvec_f = [0.0] * m
    q_f = PriorityQueue()

    max_id = -1
    max_gain = 0.0
    for v in range(n):
        gain = 0.0
        for u in range(m):
            if attr[u] == 0:
                gain += bmat[v][u]
        q_f.put(QItem(v, gain, 0))
        if gain > max_gain:
            max_id = v
            max_gain = gain
    sol_f.append(max_id)
    for u in range(m):
        bvec_f[u] = max(bvec_f[u], bmat[max_id][u])

    for it in range(1, k):
        max_id = -1
        while not q_f.empty():
            q_item = q_f.get()
            if q_item.item_id not in sol_f and q_item.iteration < it:
                gain = 0.0
                for u in range(m):
                    if u in groups[0] and bvec_f[u] < bmat[q_item.item_id][u]:
                        gain += (bmat[q_item.item_id][u] - bvec_f[u])
                if gain > 0:
                    q_f.put(QItem(q_item.item_id, gain, it))
            elif q_item.item_id not in sol_f:
                max_id = q_item.item_id
                break
        if max_id >= 0:
            sol_f.append(max_id)
            for u in range(m):
                bvec_f[u] = max(bvec_f[u], bmat[max_id][u])
        else:
            break
    opt_f = 0.0
    for u in range(m):
        if u in groups[0]:
            opt_f += bvec_f[u]

    sol_g = list()
    bvec_g = [0.0] * m
    q_g = PriorityQueue()

    max_id = -1
    max_gain = 0
    for v in range(n):
        gain = 0.0
        for u in range(m):
            if attr[u] == 1:
                gain += bmat[v][u]
        if gain > 0:
            q_g.put(QItem(v, gain, 0))
        if gain > max_gain:
            max_id = v
            max_gain = gain
    sol_g.append(max_id)
    for u in range(m):
        bvec_g[u] = max(bvec_g[u], bmat[max_id][u])

    for it in range(1, k):
        max_id = -1
        while not q_g.empty():
            q_item = q_g.get()
            if q_item.item_id not in sol_g and q_item.iteration < it:
                gain = 0.0
                for u in range(m):
                    if u in groups[1] and bvec_g[u] < bmat[q_item.item_id][u]:
                        gain += (bmat[q_item.item_id][u] - bvec_g[u])
                if gain > 0:
                    q_g.put(QItem(q_item.item_id, gain, it))
            elif q_item.item_id not in sol_g:
                max_id = q_item.item_id
                break
        if max_id >= 0:
            sol_g.append(max_id)
            for u in range(m):
                bvec_g[u] = max(bvec_g[u], bmat[max_id][u])
        else:
            break
    opt_g = 0.0
    for u in range(m):
        if u in groups[1]:
            opt_g += bvec_g[u]

    alpha_min = 0
    alpha_max = 1
    while alpha_min < (1 - math.pow(eps, 4)) * alpha_max:
        alpha = (alpha_min + alpha_max) / 2
        sol = bicriteria_smsc(bmat, attr, groups, k, alpha, beta, eps, opt_f, opt_g)
        if len(sol) == 0:
            alpha_max = alpha
        else:
            alpha_min = alpha
            sol_best = list(sol)
    stop = timeit.default_timer()
    return sol_best, (stop - start)


def bicriteria_smsc(bmat: list[list[float]], attr: list[int], groups: list[set], k: int, alpha: float, beta: float,
                    eps: float, opt_f: float, opt_g: float):
    n = len(bmat)
    m = len(bmat[0])
    caps = [alpha * opt_f, beta * opt_g]
    sol = list()
    bvec = [0.0] * n
    q = PriorityQueue()

    max_id = -1
    max_gain = 0.0
    for v in range(n):
        gain = 0
        gains = [0.0] * 2
        for j in range(2):
            for u in range(m):
                if attr[u] == j:
                    gains[j] += bmat[v][u]
            gain += min(1.0, gains[j] / caps[j])
        if gain > 1e-6:
            q.put(QItem(v, gain, 0))
        if gain > max_gain:
            max_id = v
            max_gain = gain
    sol.append(max_id)
    vals = [0.0] * 2
    for u in range(m):
        bvec[u] = max(bvec[u], bmat[max_id][u])
        vals[attr[u]] += bvec[u]
    for j in range(2):
        vals[j] = min(1.0, vals[j] / caps[j])

    for it in range(1, k):
        max_id = -1
        while not q.empty():
            q_item = q.get()
            if q_item.item_id not in sol and q_item.iteration < it:
                new_gains = [0.0] * 2
                for u in range(m):
                    if bvec[u] < bmat[q_item.item_id][u]:
                        new_gains[attr[u]] += (bmat[q_item.item_id][u] - bvec[u])
                gain = 0
                for j in range(2):
                    gain += min(new_gains[j] / caps[j], 1.0 - vals[j])
                if gain > 1e-6:
                    q.put(QItem(q_item.item_id, gain, it))
            elif q_item.item_id not in sol:
                max_id = q_item.item_id
                break
        if max_id >= 0:
            sol.append(max_id)
            for u in range(m):
                bvec[u] = max(bvec[u], bmat[max_id][u])
                vals[attr[u]] += bvec[u]
            for j in range(2):
                vals[j] = min(1.0, vals[j] / caps[j])
        else:
            break
    if sum(vals) < 2 * (1 - eps):
        return list()
    else:
        return sol


def bsm_tsgreedy_fl(bmat: list[list[float]], k: int, tau: float, attr: list[int], groups: list[set]):
    start = timeit.default_timer()
    c = len(groups)
    n = len(bmat)
    m = len(bmat[0])
    mc = [len(groups[j]) for j in range(c)]

    sol_f, time0 = greedy_fl(bmat, k)
    sol_g, time1 = saturate_fl(bmat, k, attr, groups)
    _, opt_g, _ = calc_obj_vals(bmat, sol_g, attr, groups)
    cap_g = tau * opt_g

    sol = list()
    bvec = [0.0] * n
    q = PriorityQueue()

    max_id = -1
    max_gain = 0
    for v in range(n):
        gains = [0.0] * c
        for u in range(m):
            gains[attr[u]] += bmat[v][u]
        gain = 0.0
        for j in range(c):
            gain += min(1.0, (gains[j] / mc[j]) / cap_g)
        if gain > 0:
            q.put(QItem(v, gain, 0))
        if gain > max_gain:
            max_id = v
            max_gain = gain
    sol.append(max_id)
    vals = [0.0] * c
    for u in range(m):
        bvec[u] = max(bvec[u], bmat[max_id][u])
        vals[attr[u]] += bvec[u]
    vals = [min(1.0, (vals[j] / mc[j]) / cap_g) for j in range(c)]

    it = 1
    while len(sol) < k and sum(vals) / c < 1.0 - 1e-6:
        max_id = -1
        while not q.empty():
            q_item = q.get()
            if q_item.item_id not in sol and q_item.iteration < it:
                new_gains = [0] * c
                for u in range(m):
                    if bvec[u] < bmat[q_item.item_id][u]:
                        new_gains[attr[u]] += (bmat[q_item.item_id][u] - bvec[u])
                gain = 0
                for j in range(c):
                    gain += min((new_gains[j] / mc[j]) / cap_g, 1.0 - vals[j])
                if gain > 1e-6:
                    q.put(QItem(q_item.item_id, gain, it))
            elif q_item.item_id not in sol:
                max_id = q_item.item_id
                break
        if max_id >= 0:
            sol.append(max_id)
            vals = [0.0] * c
            for u in range(m):
                bvec[u] = max(bvec[u], bmat[max_id][u])
                vals[attr[u]] += bvec[u]
            vals = [min(1.0, (vals[j] / mc[j]) / cap_g) for j in range(c)]
        else:
            break
        it += 1
    if sum(vals) / c < 1.0 - 1e-6 and len(sol) == k:
        sol.clear()
        sol.extend(sol_g)

    if len(sol) < k:
        for kk in range(k):
            if sol_f[kk] not in sol:
                sol.append(sol_f[kk])
            if len(sol) >= k:
                break
    stop = timeit.default_timer()
    return sol, (stop - start) - time1


def bsm_saturate_fl(bmat: list[list[float]], k: int, eps: float, tau: float, attr: list[int], groups: list[set]):
    start = timeit.default_timer()
    c = len(groups)
    n = len(bmat)
    m = len(attr)
    mc = [len(groups[j]) for j in range(c)]
    sol_best = list()

    sol_f, time0 = greedy_fl(bmat, k)
    opt_f0, _, _ = calc_obj_vals(bmat, sol_f, attr, groups)
    opt_f = 1.1 * opt_f0
    sol_g, time1 = saturate_fl(bmat, k, attr, groups)
    _, opt_g0, _ = calc_obj_vals(bmat, sol_g, attr, groups)
    opt_g = 1.1 * opt_g0
    cap_g = tau * opt_g

    a_min = 0.0
    a_max = 1.0
    while a_min < (1 - eps) * a_max and a_max > 0.01:
        alpha = (a_min + a_max) / 2
        cap_f = alpha * opt_f

        sol = []
        bvec = [0.0] * n
        q = PriorityQueue()

        max_id = -1
        max_gain = 0
        for v in range(n):
            gain_f = 0.0
            gains_g = [0.0] * c
            for u in range(m):
                gain_f += bmat[v][u]
                gains_g[attr[u]] += bmat[v][u]
            gain_f = min(1.0, (gain_f / m) / cap_f)
            gain_g = 0.0
            for j in range(c):
                gain_g += min(1.0, (gains_g[j] / mc[j]) / cap_g)
            gain_g /= c
            if gain_f + gain_g > 0:
                q.put(QItem(v, gain_f + gain_g, 0))
            if gain_f + gain_g > max_gain:
                max_id = v
                max_gain = gain_f + gain_g
        sol.append(max_id)
        vals_g = [0.0] * c
        for u in range(m):
            bvec[u] = max(bvec[u], bmat[max_id][u])
            vals_g[attr[u]] += bvec[u]
        val_f = min(1.0, (sum([vals_g[j] for j in range(c)]) / m) / cap_f)
        vals_g = [min(1.0, (vals_g[j] / mc[j]) / cap_g) for j in range(c)]

        for it in range(1, k):
            max_id = -1
            while not q.empty():
                q_item = q.get()
                if q_item.item_id not in sol and q_item.iteration < it:
                    new_gain = 0
                    new_gains = [0] * c
                    for u in range(m):
                        if bvec[u] < bmat[q_item.item_id][u]:
                            new_gain += (bmat[q_item.item_id][u] - bvec[u])
                            new_gains[attr[u]] += (bmat[q_item.item_id][u] - bvec[u])
                    gain_f = min((new_gain / m) / cap_f, 1.0 - val_f)
                    gain_g = 0
                    for j in range(c):
                        gain_g += min((new_gains[j] / mc[j]) / cap_g, 1.0 - vals_g[j])
                    gain_g /= c
                    if gain_f + gain_g > 1e-6:
                        q.put(QItem(q_item.item_id, gain_f + gain_g, it))
                elif q_item.item_id not in sol:
                    max_id = q_item.item_id
                    break
            if max_id >= 0:
                sol.append(max_id)
                vals_g = [0.0] * c
                for u in range(m):
                    bvec[u] = max(bvec[u], bmat[max_id][u])
                    vals_g[attr[u]] += bvec[u]
                val_f = min(1.0, (sum([vals_g[j] for j in range(c)]) / m) / cap_f)
                vals_g = [min(1.0, (vals_g[j] / mc[j]) / cap_g) for j in range(c)]
            else:
                break

        if val_f + sum(vals_g) / c < 2 * (1 - eps / c):
            a_max = alpha
        else:
            a_min = alpha
            sol_best = list(sol)
    stop = timeit.default_timer()
    return sol_best, (stop - start) - (time0 + time1)
