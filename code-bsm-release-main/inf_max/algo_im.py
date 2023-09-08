import timeit
from random import random

import networkx as nx

from max_cover.algo_mc import SetItem, greedy_mc, saturate_mc, smsc_mc, bsm_tsgreedy_mc, bsm_saturate_mc


num_iter = 10000


def read_file(graph_path: str, is_dir: bool):
    G = nx.DiGraph()

    data_lines = open(graph_path, 'r').readlines()
    header = data_lines[0].split()
    n = int(header[0])
    m = int(header[1])
    G.add_nodes_from(range(n))
    if graph_path.startswith('./data/rand') or graph_path.startswith('./data/dblp'):
        inf_pr = 0.1
    else:
        inf_pr = 0.01
    for data_line in data_lines[1:]:
        u, v = data_line.split()
        if is_dir:
            G.add_edge(int(u), int(v), weight=inf_pr)
        else:
            G.add_edge(int(u), int(v), weight=inf_pr)
            G.add_edge(int(v), int(u), weight=inf_pr)
    return n, m, G


def read_attr(attr_path: str):
    list_attr = []
    list_group = []
    
    with open(attr_path, 'r') as attr_file:
        line_no = 0
        for line in attr_file:
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
                print()
                list_attr[i] = j
                list_group[j].add(i)
            line_no += 1
            
            
    return list_attr, list_group


def est_inf(G, S):
    node_inf = dict()
    for v in list(G.nodes):
        node_inf[v] = 0
    for i in range(num_iter):
        active_set = list(S)
        active_nodes = set(S)
        while len(active_set) > 0:
            new_active_set = list()
            for u in active_set:
                for _, v, data in G.out_edges(nbunch=u, data=True):
                    if v not in active_nodes:
                        if random() < data['weight']:
                            active_nodes.add(v)
                            new_active_set.append(v)
            active_set = new_active_set
        for v in active_nodes:
            node_inf[v] += 1
    for v in list(G.nodes):
        node_inf[v] /= num_iter
    return node_inf


def calc_obj_vals(inf: dict, list_attr: list[int], list_groups: list[set]):
    val_f = sum(inf.values()) / len(list_attr)
    vals_g = []
    c = len(list_groups)
    for j in range(c):
        vals_g.append(0)
    for user, prob in inf.items():
        j = list_attr[user]
        vals_g[j] += prob
    for j in range(c):
        vals_g[j] /= len(list_groups[j])
    val_g = min(vals_g)
    return val_f, val_g, vals_g


def generate_items(n: int, ris: list[set]):
    list_items = []
    for i in range(n):
        list_items.append(SetItem(i, set()))
    for i in range(len(ris)):
        for v in ris[i]:
            list_items[v].elem.add(i)
    return list_items


def generate_attr(nodes: list[int], user_attr: list[int], user_groups: list[set]):
    rr_size = len(nodes)
    c = len(user_groups)
    list_attr = []
    list_group = []
    for i in range(rr_size):
        list_attr.append(-1)
    for j in range(c):
        list_group.append(set())
    for i in range(rr_size):
        list_attr[i] = user_attr[nodes[i]]
        list_group[user_attr[nodes[i]]].add(i)
    return list_attr, list_group


def greedy_im(ris: list[set], k: int, n: int):
    start = timeit.default_timer()
    items = generate_items(n, ris)
    sol, _, _ = greedy_mc(items, k)
    end = timeit.default_timer()
    print (sol)
    return sol, (end - start)


def saturate_im(ris: list[set], nodes: list[int], k: int, n: int, user_attrs: list[int], user_groups: list[set]):
    start = timeit.default_timer()
    items = generate_items(n, ris)
    attrs, groups = generate_attr(nodes, user_attrs, user_groups)
    sol, _, _ = saturate_mc(items, k, attrs, groups)
    end = timeit.default_timer()
    return sol, (end - start)


def smsc_im(ris: list[set], nodes: list[int], k: int, n: int, beta: float, user_attrs: list[int], user_groups: list[set]):
    start = timeit.default_timer()
    items = generate_items(n, ris)
    attrs, groups = generate_attr(nodes, user_attrs, user_groups)
    sol, _, _ = smsc_mc(items, k, beta, attrs, groups)
    end = timeit.default_timer()
    return sol, (end - start)


def bsm_tsgreedy_im(ris: list[set], nodes: list[int], k: int, n: int, tau: float, user_attrs: list[int], user_groups: list[set]):
    start = timeit.default_timer()
    items = generate_items(n, ris)
    attrs, groups = generate_attr(nodes, user_attrs, user_groups)
    end = timeit.default_timer()
    sol, _, time2 = bsm_tsgreedy_mc(items, k, tau, attrs, groups)
    return sol, (end - start) + time2


def bsm_saturate_im(ris: list[set], nodes: list[int], k: int, n: int, eps: float, tau: float, user_attrs: list[int], user_groups: list[set]):
    start = timeit.default_timer()
    items = generate_items(n, ris)
    attrs, groups = generate_attr(nodes, user_attrs, user_groups)
    end = timeit.default_timer()
    sol, _, time2 = bsm_saturate_mc(items, k, eps, tau, attrs, groups)
    return sol, (end - start) + time2
