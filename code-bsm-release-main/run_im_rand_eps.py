import numpy

from inf_max.algo_im import bsm_saturate_im, read_file, read_attr, est_inf, calc_obj_vals
from inf_max.imm import IMM

num_nodes, _, graph = read_file("./data/rand_graph/im_rand_c2_edges.txt", is_dir=False)
attrs, groups = read_attr('./data/rand_graph/im_rand_c2_attr.txt')
output_file = open('./results/im_results_rand_c2_eps.csv', 'w')
output_file.write('algorithm,k,eps,f,g,time(s)\n')

k = 5
tau = 0.8

inst_imm = IMM(graph, False, num_nodes, k, 0.1)
nodes, ris = inst_imm.run()
print(len(ris))

eps_vals = numpy.arange(0.01, 1.0, 0.01)

for eps in eps_vals:
    sol, time = bsm_saturate_im(ris, nodes, k, num_nodes, eps, tau, attrs, groups)
    dict_inf = est_inf(graph, sol)
    f, g, _ = calc_obj_vals(dict_inf, attrs, groups)
    output_file.write('BSM-Saturate,' + str(k) + ',' + str(eps) + ',' + str(f) + ',' + str(g) + ',' + '-' + '\n')

output_file.close()

num_nodes, _, graph = read_file("./data/rand_graph/im_rand_c4_edges.txt", is_dir=False)
attrs, groups = read_attr('./data/rand_graph/im_rand_c4_attr.txt')
output_file = open('./results/im_results_rand_c4_eps.csv', 'w')
output_file.write('algorithm,k,eps,f,g,time(s)\n')

inst_imm = IMM(graph, False, num_nodes, k, 0.1)
nodes, ris = inst_imm.run()
print(len(ris))

eps_vals = numpy.arange(0.01, 1.0, 0.01)

for eps in eps_vals:
    sol, time = bsm_saturate_im(ris, nodes, k, num_nodes, eps, tau, attrs, groups)
    dict_inf = est_inf(graph, sol)
    f, g, _ = calc_obj_vals(dict_inf, attrs, groups)
    output_file.write('BSM-Saturate,' + str(k) + ',' + str(eps) + ',' + str(f) + ',' + str(g) + ',' + '-' + '\n')

output_file.close()
