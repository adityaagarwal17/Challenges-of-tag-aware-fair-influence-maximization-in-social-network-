import functools
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


def calc_obj_vals(bmat, sol):
    m = len(bmat[0])
    bvec = [0.0] * m
    for v in sol:
        for u in range(m):
            bvec[u] = max(bvec[u], bmat[v][u])
    val_f = sum(bvec) / m
    val_g = min(bvec)
    return val_f, val_g


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
    max_dist = 0.0
    for i in range(n):
        for j in range(m):
            max_dist = max(max_dist, dist2(list_items[i], list_users[j]))
    mat = [[0.0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            b_ij = max(0.0, (max_dist / 8 - dist2(list_items[i], list_users[j])) * 10)
            mat[i][j] = b_ij
    return mat


def greedy_fl_indiv(bmat: list[list[float]], k: int):
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


def saturate_fl_indiv(bmat: list[list[float]], k: int):
    start = timeit.default_timer()
    sol_best = list()
    n = len(bmat)
    m = len(bmat[0])

    eps = 0.05

    g_min = 0.0
    g_max = 0.0
    for v in range(n):
        g_max = max(g_max, max(bmat[v]))
    while g_min < (1 - eps) * g_max:
        g_cur = (g_min + g_max) / 2

        sol = list()
        bvec = [0.0] * m
        q = PriorityQueue()

        max_id = -1
        max_gain = 0
        for v in range(n):
            gain = 0.0
            for u in range(m):
                gain += min(g_cur, bmat[v][u])
            if gain > 0:
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
                    gain = 0.0
                    for u in range(m):
                        if bvec[u] < bmat[q_item.item_id][u] and bvec[u] < g_cur:
                            gain += min(bmat[q_item.item_id][u] - bvec[u], g_cur - bvec[u])
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
        is_covered = True
        for u in range(m):
            if bvec[u] < g_cur - 1e-6:
                is_covered = False
                break
        if is_covered:
            g_min = g_cur
            sol_best = list(sol)
        else:
            g_max = g_cur
    stop = timeit.default_timer()
    return sol_best, (stop - start)


def bsm_tsgreedy_fl_indiv(bmat: list[list[float]], k: int, tau: float):
    start = timeit.default_timer()
    n = len(bmat)
    m = len(bmat[0])

    sol_f, time0 = greedy_fl_indiv(bmat, k)
    sol_g, time1 = saturate_fl_indiv(bmat, k)
    _, opt_g = calc_obj_vals(bmat, sol_g)
    cap_g = tau * opt_g

    sol = list()
    bvec = [0.0] * m
    q = PriorityQueue()

    max_id = -1
    max_gain = 0
    for v in range(n):
        gain = 0.0
        for u in range(m):
            gain += min(cap_g, bmat[v][u])
        if gain > 0:
            q.put(QItem(v, gain, 0))
        if gain > max_gain:
            max_id = v
            max_gain = gain
    sol.append(max_id)
    for u in range(m):
        bvec[u] = max(bvec[u], bmat[max_id][u])
    vals = [min(1.0, (bvec[u] / cap_g)) for u in range(m)]

    it = 1
    while len(sol) < k and sum(vals) / m < 1.0 - 1e-6:
        max_id = -1
        while not q.empty():
            q_item = q.get()
            if q_item.item_id not in sol and q_item.iteration < it:
                gain = 0.0
                for u in range(m):
                    if bvec[u] < bmat[q_item.item_id][u] and bvec[u] < cap_g:
                        gain += min(bmat[q_item.item_id][u] - bvec[u], cap_g - bvec[u])
                if gain > 1e-6:
                    q.put(QItem(q_item.item_id, gain, it))
            elif q_item.item_id not in sol:
                max_id = q_item.item_id
                break
        if max_id >= 0:
            sol.append(max_id)
            for u in range(m):
                bvec[u] = max(bvec[u], bmat[max_id][u])
            vals = [min(1.0, (bvec[u] / cap_g)) for u in range(m)]
        else:
            break
        it += 1
    if sum(vals) / m < 1.0 - 1e-6 and len(sol) == k:
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


def bsm_saturate_fl_indiv(bmat: list[list[float]], k: int, eps: float, tau: float):
    start = timeit.default_timer()
    n = len(bmat)
    m = len(bmat[0])
    sol_best = list()

    sol_f, time0 = greedy_fl_indiv(bmat, k)
    opt_f0, _ = calc_obj_vals(bmat, sol_f)
    opt_f = 1.1 * opt_f0
    sol_g, time1 = saturate_fl_indiv(bmat, k)
    _, opt_g0 = calc_obj_vals(bmat, sol_g)
    opt_g = 1.05 * opt_g0
    cap_g = tau * opt_g

    a_min = 0.0
    a_max = 1.0
    while a_min < (1 - eps) * a_max and a_max > 0.01:
        alpha = (a_min + a_max) / 2
        cap_f = alpha * opt_f

        sol = []
        bvec = [0.0] * m
        q = PriorityQueue()

        max_id = -1
        max_gain = 0
        for v in range(n):
            gain_f = min(1.0, (sum(bmat[v]) / m) / cap_f)
            gain_g = 0.0
            for u in range(m):
                gain_g += min(1.0, bmat[v][u] / cap_g)
            gain_g /= m
            if gain_f + gain_g > 0:
                q.put(QItem(v, gain_f + gain_g, 0))
            if gain_f + gain_g > max_gain:
                max_id = v
                max_gain = gain_f + gain_g
        sol.append(max_id)
        for u in range(m):
            bvec[u] = max(bvec[u], bmat[max_id][u])
        val_f = min(1.0, (sum(bvec) / m) / cap_f)
        vals_g = [0.0] * m
        for u in range(m):
            vals_g[u] = min(1.0, bvec[u] / cap_g)

        for it in range(1, k):
            max_id = -1
            while not q.empty():
                q_item = q.get()
                if q_item.item_id not in sol and q_item.iteration < it:
                    new_gain_f = 0.0
                    new_gains_g = [0.0] * m
                    for u in range(m):
                        if bvec[u] < bmat[q_item.item_id][u]:
                            new_gain_f += (bmat[q_item.item_id][u] - bvec[u])
                            new_gains_g[u] = bmat[q_item.item_id][u] - bvec[u]
                    gain_f = min((new_gain_f / m) / cap_f, 1.0 - val_f)
                    gain_g = 0
                    for u in range(m):
                        gain_g += min(new_gains_g[u] / cap_g, 1.0 - vals_g[u])
                    gain_g /= m
                    if gain_f + gain_g > 1e-6:
                        q.put(QItem(q_item.item_id, gain_f + gain_g, it))
                elif q_item.item_id not in sol:
                    max_id = q_item.item_id
                    break
            if max_id >= 0:
                sol.append(max_id)
                for u in range(m):
                    bvec[u] = max(bvec[u], bmat[max_id][u])
                val_f = min(1.0, (sum(bvec) / m) / cap_f)
                vals_g = [0.0] * m
                for u in range(m):
                    vals_g[u] = min(1.0, bvec[u] / cap_g)
            else:
                break

        if val_f + sum(vals_g) / m < 2 * (1 - eps / m):
            a_max = alpha
        else:
            a_min = alpha
            sol_best = list(sol)
    stop = timeit.default_timer()
    return sol_best, (stop - start) - (time0 + time1)
