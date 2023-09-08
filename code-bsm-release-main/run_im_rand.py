import numpy

from inf_max.algo_im import greedy_im, saturate_im, smsc_im, bsm_tsgreedy_im, bsm_saturate_im, read_file, read_attr, est_inf, calc_obj_vals
from inf_max.imm import IMM

num_nodes, _, graph = read_file("./data/rand_graph/im_rand_c2_edges.txt", is_dir=False)
attrs, groups = read_attr('./data/rand_graph/im_rand_c2_attr.txt')
output_file = open('./results/im_results_rand_c2.csv', 'w')
output_file.write('algorithm,k,tau,f,g,time(s)\n')

k = 5
eps = 0.05

inst_imm = IMM(graph, False, num_nodes, k, 0.1)
nodes, ris = inst_imm.run()
print(len(ris))

sol, time = greedy_im(ris, k, num_nodes)
dict_inf = est_inf(graph, sol)
f, g, _ = calc_obj_vals(dict_inf, attrs, groups)
output_file.write('Greedy,' + str(k) + ',' + 'N/A' + ',' + str(f) + ',' + str(g) + ',' + str(time) + '\n')

sol, time = saturate_im(ris, nodes, k, num_nodes, attrs, groups)
dict_inf = est_inf(graph, sol)
f, g, _ = calc_obj_vals(dict_inf, attrs, groups)
output_file.write('Saturate,' + str(k) + ',' + 'N/A' + ',' + str(f) + ',' + str(g) + ',' + str(time) + '\n')

taus = numpy.arange(0.1, 1.0, 0.1)

for tau in taus:
    total_time = 0
    for r in range(10):
        sol, time = smsc_im(ris, nodes, k, num_nodes, tau, attrs, groups)
        total_time += time
    dict_inf = est_inf(graph, sol)
    f, g, _ = calc_obj_vals(dict_inf, attrs, groups)
    output_file.write('SMSC,' + str(k) + ',' + str(tau) + ',' + str(f) + ',' + str(g) + ',' + str(total_time / 10) + '\n')

for tau in taus:
    total_time = 0
    for r in range(10):
        sol, time = bsm_tsgreedy_im(ris, nodes, k, num_nodes, tau, attrs, groups)
        total_time += time
    dict_inf = est_inf(graph, sol)
    f, g, _ = calc_obj_vals(dict_inf, attrs, groups)
    output_file.write('BSM-TSGreedy,' + str(k) + ',' + str(tau) + ',' + str(f) + ',' + str(g) + ',' + str(total_time / 10) + '\n')

for tau in taus:
    total_time = 0
    for r in range(10):
        sol, time = bsm_saturate_im(ris, nodes, k, num_nodes, eps, tau, attrs, groups)
        total_time += time
    dict_inf = est_inf(graph, sol)
    f, g, _ = calc_obj_vals(dict_inf, attrs, groups)
    output_file.write('BSM-Saturate,' + str(k) + ',' + str(tau) + ',' + str(f) + ',' + str(g) + ',' + str(total_time / 10) + '\n')

output_file.close()

num_nodes, _, graph = read_file("./data/rand_graph/im_rand_c4_edges.txt", is_dir=False)
attrs, groups = read_attr('./data/rand_graph/im_rand_c4_attr.txt')
output_file = open('./results/im_results_rand_c4.csv', 'w')
output_file.write('algorithm,k,tau,f,g,time(s)\n')

inst_imm = IMM(graph, False, num_nodes, k, 0.1)
nodes, ris = inst_imm.run()
print(len(ris))

sol, time = greedy_im(ris, k, num_nodes)
dict_inf = est_inf(graph, sol)
f, g, _ = calc_obj_vals(dict_inf, attrs, groups)
output_file.write('Greedy,' + str(k) + ',' + 'N/A' + ',' + str(f) + ',' + str(g) + ',' + str(time) + '\n')

sol, time = saturate_im(ris, nodes, k, num_nodes, attrs, groups)
dict_inf = est_inf(graph, sol)
f, g, _ = calc_obj_vals(dict_inf, attrs, groups)
output_file.write('Saturate,' + str(k) + ',' + 'N/A' + ',' + str(f) + ',' + str(g) + ',' + str(time) + '\n')

taus = numpy.arange(0.1, 1.0, 0.1)

for tau in taus:
    total_time = 0
    for r in range(10):
        sol, time = bsm_tsgreedy_im(ris, nodes, k, num_nodes, tau, attrs, groups)
        total_time += time
    dict_inf = est_inf(graph, sol)
    f, g, _ = calc_obj_vals(dict_inf, attrs, groups)
    output_file.write('BSM-TSGreedy,' + str(k) + ',' + str(tau) + ',' + str(f) + ',' + str(g) + ',' + str(total_time / 10) + '\n')

for tau in taus:
    total_time = 0
    for r in range(10):
        sol, time = bsm_saturate_im(ris, nodes, k, num_nodes, eps, tau, attrs, groups)
        total_time += time
    dict_inf = est_inf(graph, sol)
    f, g, _ = calc_obj_vals(dict_inf, attrs, groups)
    output_file.write('BSM-Saturate,' + str(k) + ',' + str(tau) + ',' + str(f) + ',' + str(g) + ',' + str(total_time / 10) + '\n')

output_file.close()
