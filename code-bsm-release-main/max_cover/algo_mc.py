import functools
import math
import timeit
from queue import PriorityQueue


class SetItem:
    def __init__(self, item_id: int, elem: set):
        self.item_id = item_id
        self.elem = elem


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


def read_items(input_path: str, is_directed: bool):
    list_items = []
    with open(input_path, 'r') as input_file:
        line_no = 0
        for line in input_file:
            tokens = line.strip().split(' ')
            if line_no == 0:
                n = int(tokens[0])
                for i in range(n):
                    list_items.append(SetItem(i, set()))
                    list_items[i].elem.add(i)
            else:
                s = int(tokens[0])
                t = int(tokens[1])
                if not is_directed:
                    list_items[s].elem.add(t)
                    list_items[t].elem.add(s)
                else:
                    list_items[s].elem.add(t)
            line_no += 1
    return list_items


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


def calc_obj_vals(coverage, list_attr, list_groups):
    val_f = len(coverage) / len(list_attr)
    vals_g = []
    c = len(list_groups)
    for j in range(c):
        vals_g.append(0)
    for user_id in coverage:
        j = list_attr[user_id]
        vals_g[j] += 1
    for j in range(c):
        vals_g[j] /= len(list_groups[j])
    val_g = min(vals_g)
    return val_f, val_g, vals_g


def greedy_mc(items: list[SetItem], k: int):
    start = timeit.default_timer()
    sol = list()
    cov = set()
    q = PriorityQueue()

    max_id = -1
    max_gain = 0
    for v in items:
        gain = len(v.elem)
        q.put(QItem(v.item_id, gain, 0))
        if gain > max_gain:
            max_id = v.item_id
            max_gain = gain
    sol.append(max_id)
    cov.update(items[max_id].elem)

    for it in range(1, k):
        max_id = -1
        while not q.empty():
            q_item = q.get()
            if q_item.item_id not in sol and q_item.iteration < it:
                gain = 0
                for u in items[q_item.item_id].elem:
                    if u not in cov:
                        gain += 1
                if gain > 0:
                    q.put(QItem(q_item.item_id, gain, it))
            elif q_item.item_id not in sol:
                max_id = q_item.item_id
                break
        if max_id >= 0:
            sol.append(max_id)
            cov.update(items[max_id].elem)
        else:
            break
    stop = timeit.default_timer()
    return sol, cov, (stop - start)


def saturate_mc(items: list[SetItem], k: int, attr: list[int], groups: list[set]):
    start = timeit.default_timer()
    sol_best = list()
    c = len(groups)
    eps = 0.05
    mc = [len(groups[j]) for j in range(c)]

    g_min = 0
    g_max = 1
    while g_min < (1 - eps) * g_max:
        g_cur = (g_min + g_max) / 2
        caps = [max(1, math.floor(g_cur * mc[j])) for j in range(c)]

        sol = list()
        covs = [set() for _ in range(c)]
        q = PriorityQueue()

        max_id = -1
        max_gain = 0
        for v in items:
            gain = 0
            for j in range(c):
                gain_j = len(v.elem.intersection(groups[j]))
                if gain_j <= caps[j]:
                    gain += gain_j
                else:
                    gain += caps[j]
            if gain > 0:
                q.put(QItem(v.item_id, gain, 0))
            if gain > max_gain:
                max_id = v.item_id
                max_gain = gain
        sol.append(max_id)
        for u in items[max_id].elem:
            covs[attr[u]].add(u)

        for it in range(1, k):
            max_id = -1
            while not q.empty():
                q_item = q.get()
                if q_item.item_id not in sol and q_item.iteration < it:
                    gains = [0] * c
                    for u in items[q_item.item_id].elem:
                        if u not in covs[attr[u]]:
                            gains[attr[u]] += 1
                    gain = 0
                    for j in range(c):
                        gain += min(gains[j], max(0, caps[j] - len(covs[j])))
                    if gain > 0:
                        q.put(QItem(q_item.item_id, gain, it))
                elif q_item.item_id not in sol:
                    max_id = q_item.item_id
                    break
            if max_id >= 0:
                sol.append(max_id)
                for u in items[max_id].elem:
                    covs[attr[u]].add(u)
            else:
                break
        is_covered = True
        for j in range(c):
            if len(covs[j]) < caps[j]:
                is_covered = False
                break
        if is_covered:
            g_min = g_cur
            sol_best = list(sol)
        else:
            g_max = g_cur
    stop = timeit.default_timer()
    cov = set()
    for v in sol_best:
        cov.update(items[v].elem)

    return sol_best, cov, (stop - start)


def smsc_mc(items: list[SetItem], k: int, beta: float, attr: list[int], groups: list[set]):
    start = timeit.default_timer()
    sol_best = list()
    eps = 1 / math.e
    if len(groups) > 2:
        return None

    sol_f = list()
    cov_f = set()
    q_f = PriorityQueue()

    max_id = -1
    max_gain = 0
    for v in items:
        gain = len(v.elem.intersection(groups[0]))
        if gain > 0:
            q_f.put(QItem(v.item_id, gain, 0))
        if gain > max_gain:
            max_id = v.item_id
            max_gain = gain
    sol_f.append(max_id)
    cov_f.update(items[max_id].elem)

    for it in range(1, k):
        max_id = -1
        while not q_f.empty():
            q_item = q_f.get()
            if q_item.item_id not in sol_f and q_item.iteration < it:
                gain = 0
                for u in items[q_item.item_id].elem:
                    if u not in cov_f and u in groups[0]:
                        gain += 1
                if gain > 0:
                    q_f.put(QItem(q_item.item_id, gain, it))
            elif q_item.item_id not in sol_f:
                max_id = q_item.item_id
                break
        if max_id >= 0:
            sol_f.append(max_id)
            cov_f.update(items[max_id].elem)
        else:
            break
    opt_f = len(cov_f.intersection(groups[0]))

    sol_g = list()
    cov_g = set()
    q_g = PriorityQueue()

    max_id = -1
    max_gain = 0
    for v in items:
        gain = len(v.elem.intersection(groups[1]))
        if gain > 0:
            q_g.put(QItem(v.item_id, gain, 0))
        if gain > max_gain:
            max_id = v.item_id
            max_gain = gain
    sol_g.append(max_id)
    cov_g.update(items[max_id].elem)

    for it in range(1, k):
        max_id = -1
        while not q_g.empty():
            q_item = q_g.get()
            if q_item.item_id not in sol_g and q_item.iteration < it:
                gain = 0
                for u in items[q_item.item_id].elem:
                    if u not in cov_g and u in groups[1]:
                        gain += 1
                if gain > 0:
                    q_g.put(QItem(q_item.item_id, gain, it))
            elif q_item.item_id not in sol_g:
                max_id = q_item.item_id
                break
        if max_id >= 0:
            sol_g.append(max_id)
            cov_g.update(items[max_id].elem)
        else:
            break
    opt_g = len(cov_g.intersection(groups[1]))

    alpha_min = 0
    alpha_max = 1
    while alpha_min < (1 - math.pow(eps, 4)) * alpha_max:
        alpha = (alpha_min + alpha_max) / 2
        sol = bicriteria_smsc(items, attr, groups, k, alpha, beta, eps, opt_f, opt_g)
        if len(sol) == 0:
            alpha_max = alpha
        else:
            alpha_min = alpha
            sol_best = list(sol)
    stop = timeit.default_timer()
    cov = set()
    for v in sol_best:
        cov.update(items[v].elem)

    return sol_best, cov, (stop - start)


def bicriteria_smsc(items: list[SetItem], attr: list[int], groups: list[set], k: int, alpha: float, beta: float,
                    eps: float, opt_f: float, opt_g: float):
    caps = [alpha * opt_f, beta * opt_g]
    sol = list()
    covs = [set(), set()]
    q = PriorityQueue()

    max_id = -1
    max_gain = 0
    for v in items:
        gain = 0
        for j in range(2):
            gain += min(1.0, len(v.elem.intersection(groups[j])) / caps[j])
        if gain > 1e-6:
            q.put(QItem(v.item_id, gain, 0))
        if gain > max_gain:
            max_id = v.item_id
            max_gain = gain
    sol.append(max_id)
    for u in items[max_id].elem:
        covs[attr[u]].add(u)
    vals = [min(1.0, len(covs[0]) / caps[0]), min(1.0, len(covs[1]) / caps[1])]

    for it in range(1, k):
        max_id = -1
        while not q.empty():
            q_item = q.get()
            if q_item.item_id not in sol and q_item.iteration < it:
                new_covs = [0, 0]
                for u in items[q_item.item_id].elem:
                    if u not in covs[attr[u]]:
                        new_covs[attr[u]] += 1
                gain = 0
                for j in range(2):
                    gain += min(new_covs[j] / caps[j], max(0.0, 1.0 - len(covs[j]) / caps[j]))
                if gain > 1e-6:
                    q.put(QItem(q_item.item_id, gain, it))
            elif q_item.item_id not in sol:
                max_id = q_item.item_id
                break
        if max_id >= 0:
            sol.append(max_id)
            for u in items[max_id].elem:
                covs[attr[u]].add(u)
            vals = [min(1.0, len(covs[0]) / caps[0]), min(1.0, len(covs[1]) / caps[1])]
        else:
            break
    if sum(vals) < 2 * (1 - eps):
        return list()
    else:
        return sol


def bsm_tsgreedy_mc(items: list[SetItem], k: int, tau: float, attr: list[int], groups: list[set]):
    c = len(groups)
    mc = [len(groups[j]) for j in range(c)]

    sol_f, cov_f, time0 = greedy_mc(items, k)
    sol_g, cov_g, time1 = saturate_mc(items, k, attr, groups)

    start = timeit.default_timer()
    opt_g = min([(len(cov_g.intersection(groups[j])) / mc[j]) for j in range(c)])
    cap_g = tau * opt_g

    sol = list()
    covs = [set() for _ in range(c)]
    q = PriorityQueue()

    max_id = -1
    max_gain = 0
    for v in items:
        gain = 0
        for j in range(c):
            gain += min(1.0, (len(v.elem.intersection(groups[j])) / mc[j]) / cap_g)
        if gain > 0:
            q.put(QItem(v.item_id, gain, 0))
        if gain > max_gain:
            max_id = v.item_id
            max_gain = gain
    sol.append(max_id)
    for u in items[max_id].elem:
        covs[attr[u]].add(u)
    vals = [min(1.0, (len(covs[j]) / mc[j]) / cap_g) for j in range(c)]

    it = 1
    while len(sol) < k and sum(vals) / c < 1.0 - 1e-6:
        max_id = -1
        while not q.empty():
            q_item = q.get()
            if q_item.item_id not in sol and q_item.iteration < it:
                new_covs = [0] * c
                for u in items[q_item.item_id].elem:
                    if u not in covs[attr[u]]:
                        new_covs[attr[u]] += 1
                gain = 0
                for j in range(c):
                    gain += min((new_covs[j] / mc[j]) / cap_g, 1.0 - vals[j])
                if gain > 1e-6:
                    q.put(QItem(q_item.item_id, gain, it))
            elif q_item.item_id not in sol:
                max_id = q_item.item_id
                break
        if max_id >= 0:
            sol.append(max_id)
            for u in items[max_id].elem:
                covs[attr[u]].add(u)
            vals = [min(1.0, (len(covs[j]) / mc[j]) / cap_g) for j in range(c)]
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
    cov = set()
    for v in sol:
        cov.update(items[v].elem)
    return sol, cov, (stop - start) + time0


def bsm_saturate_mc(items: list[SetItem], k: int, eps: float, tau: float, attr: list[int], groups: list[set]):
    c = len(groups)
    m = len(attr)
    mc = [len(groups[j]) for j in range(c)]
    sol_best = list()

    sol_f, cov_f, time0 = greedy_mc(items, k)
    sol_g, cov_g, time1 = saturate_mc(items, k, attr, groups)

    start = timeit.default_timer()
    opt_f = 1.1 * len(cov_f) / len(attr)
    opt_g = 1.1 * min([(len(cov_g.intersection(groups[j])) / mc[j]) for j in range(c)])
    cap_g = tau * opt_g

    a_min = 0.0
    a_max = 1.0
    while a_min < (1 - eps) * a_max and a_max > 0.01:
        alpha = (a_min + a_max) / 2
        cap_f = alpha * opt_f

        sol = []
        covs = [set() for _ in range(c)]
        q = PriorityQueue()

        max_id = -1
        max_gain = 0
        for v in items:
            gain_f = min(1.0, (len(v.elem) / m) / cap_f)
            gain_g = 0
            for j in range(c):
                gain_g += min(1.0, (len(v.elem.intersection(groups[j])) / mc[j]) / cap_g)
            gain_g /= c
            if gain_f + gain_g > 0:
                q.put(QItem(v.item_id, gain_f + gain_g, 0))
            if gain_f + gain_g > max_gain:
                max_id = v.item_id
                max_gain = gain_f + gain_g
        sol.append(max_id)
        for u in items[max_id].elem:
            covs[attr[u]].add(u)
        val_f = min(1.0, (sum([len(covs[j]) for j in range(c)]) / m) / cap_f)
        vals_g = [min(1.0, (len(covs[j]) / mc[j]) / cap_g) for j in range(c)]

        for it in range(1, k):
            max_id = -1
            while not q.empty():
                q_item = q.get()
                if q_item.item_id not in sol and q_item.iteration < it:
                    new_cov = 0
                    new_covs = [0] * c
                    for u in items[q_item.item_id].elem:
                        if u not in covs[attr[u]]:
                            new_cov += 1
                            new_covs[attr[u]] += 1
                    gain_f = min((new_cov / m) / cap_f, 1.0 - val_f)
                    gain_g = 0
                    for j in range(c):
                        gain_g += min((new_covs[j] / mc[j]) / cap_g, 1.0 - vals_g[j])
                    gain_g /= c
                    if gain_f + gain_g > 1e-6:
                        q.put(QItem(q_item.item_id, gain_f + gain_g, it))
                elif q_item.item_id not in sol:
                    max_id = q_item.item_id
                    break
            if max_id >= 0:
                sol.append(max_id)
                for u in items[max_id].elem:
                    covs[attr[u]].add(u)
                val_f = min(1.0, (sum([len(covs[j]) for j in range(c)]) / m) / cap_f)
                vals_g = [min(1.0, (len(covs[j]) / mc[j]) / cap_g) for j in range(c)]
            else:
                break

        if val_f + sum(vals_g) / c < 2 * (1 - eps / c):
            a_max = alpha
        else:
            a_min = alpha
            sol_best = list(sol)
    stop = timeit.default_timer()
    cov = set()
    for v in sol_best:
        cov.update(items[v].elem)
    return sol_best, cov, (stop - start)
