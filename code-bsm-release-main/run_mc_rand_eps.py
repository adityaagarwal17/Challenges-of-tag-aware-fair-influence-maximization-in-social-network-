import numpy

from max_cover.algo_mc import bsm_saturate_mc, read_items, read_attr, calc_obj_vals

# Experiments on random graphs
items = read_items('./data/rand_graph/mc_rand_c2_edges.txt', is_directed=False)
attrs, groups = read_attr('./data/rand_graph/mc_rand_c2_attr.txt')
output_file = open('./results/mc_results_rand_c2_eps.csv', 'w')
output_file.write('algorithm,k,eps,f,g,time(s)\n')

k = 5
tau = 0.8

eps_vals = numpy.arange(0.01, 1.0, 0.01)

for eps in eps_vals:
    _, cov, time = bsm_saturate_mc(items, k, eps, tau, attrs, groups)
    f, g, _ = calc_obj_vals(cov, attrs, groups)
    output_file.write('BSM-Saturate,' + str(k) + ',' + str(eps) + ',' + str(f) + ',' + str(g) + ',' + '-' + '\n')

items.clear()
attrs.clear()
groups.clear()
output_file.close()

items = read_items('./data/rand_graph/mc_rand_c4_edges.txt', is_directed=False)
attrs, groups = read_attr('./data/rand_graph/mc_rand_c4_attr.txt')
output_file = open('./results/mc_results_rand_c4_eps.csv', 'w')
output_file.write('algorithm,k,eps,f,g,time(s)\n')

eps_vals = numpy.arange(0.01, 1.0, 0.01)

for eps in eps_vals:
    _, cov, time = bsm_saturate_mc(items, k, eps, tau, attrs, groups)
    f, g, _ = calc_obj_vals(cov, attrs, groups)
    output_file.write('BSM-Saturate,' + str(k) + ',' + str(eps) + ',' + str(f) + ',' + str(g) + ',' + '-' + '\n')

output_file.close()
