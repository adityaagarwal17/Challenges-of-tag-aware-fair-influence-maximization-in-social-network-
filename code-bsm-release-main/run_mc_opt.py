import numpy

from max_cover.algo_mc import read_items, read_attr, calc_obj_vals
from max_cover.algo_mc_opt import max_cover_ip, robust_max_cover_ip, bsm_max_cover_ip

# Experiments on random graphs
items = read_items('./data/rand_graph/mc_rand_c2_edges.txt', is_directed=False)
attrs, groups = read_attr('./data/rand_graph/mc_rand_c2_attr.txt')
output_file = open('./results/mc_results_rand_c2_optimal.csv', 'w')
output_file.write('algorithm,k,tau,f,g,time(s)\n')

k = 5

_, cov, time = max_cover_ip(items, k)
f, g, _ = calc_obj_vals(cov, attrs, groups)
output_file.write('OPT_f,' + str(k) + ',' + 'N/A' + ',' + str(f) + ',' + str(g) + ',' + str(time) + '\n')

_, cov, time = robust_max_cover_ip(items, k, attrs, groups)
f, g, _ = calc_obj_vals(cov, attrs, groups)
output_file.write('OPT_g,' + str(k) + ',' + 'N/A' + ',' + str(f) + ',' + str(g) + ',' + str(time) + '\n')

opt_g = g
taus = numpy.arange(0.1, 1.0, 0.1)
for tau in taus:
    _, cov, time = bsm_max_cover_ip(items, k, tau, opt_g, attrs, groups)
    f, g, _ = calc_obj_vals(cov, attrs, groups)
    output_file.write('BSM-Optimal,' + str(k) + ',' + str(tau) + ',' + str(f) + ',' + str(g) + ',' + str(time) + '\n')

items.clear()
attrs.clear()
groups.clear()
output_file.close()

items = read_items('./data/rand_graph/mc_rand_c4_edges.txt', is_directed=False)
attrs, groups = read_attr('./data/rand_graph/mc_rand_c4_attr.txt')
output_file = open('./results/mc_results_rand_c4_optimal.csv', 'w')
output_file.write('algorithm,k,tau,f,g,time(s)\n')

_, cov, time = max_cover_ip(items, k)
f, g, _ = calc_obj_vals(cov, attrs, groups)
output_file.write('OPT_f,' + str(k) + ',' + 'N/A' + ',' + str(f) + ',' + str(g) + ',' + str(time) + '\n')

_, cov, time = robust_max_cover_ip(items, k, attrs, groups)
f, g, _ = calc_obj_vals(cov, attrs, groups)
output_file.write('OPT_g,' + str(k) + ',' + 'N/A' + ',' + str(f) + ',' + str(g) + ',' + str(time) + '\n')

opt_g = g
taus = numpy.arange(0.1, 1.0, 0.1)
for tau in taus:
    _, cov, time = bsm_max_cover_ip(items, k, tau, opt_g, attrs, groups)
    f, g, _ = calc_obj_vals(cov, attrs, groups)
    output_file.write('BSM-Optimal,' + str(k) + ',' + str(tau) + ',' + str(f) + ',' + str(g) + ',' + str(time) + '\n')

output_file.close()
