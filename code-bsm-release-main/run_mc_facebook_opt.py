import numpy

from max_cover.algo_mc import read_items, read_attr, calc_obj_vals
from max_cover.algo_mc_opt import max_cover_ip, robust_max_cover_ip, bsm_max_cover_ip

# Experiments on facebook graphs
items = read_items('./data/facebook/facebook-edges.txt', is_directed=False)
attrs, groups = read_attr('./data/facebook/facebook-attr1.txt')
output_file = open('./results/mc_results_facebook_attr1_optimal.csv', 'w')
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

items = read_items('./data/facebook/facebook-edges.txt', is_directed=False)
attrs, groups = read_attr('./data/facebook/facebook-attr2.txt')
output_file = open('./results/mc_results_facebook_attr2_optimal.csv', 'w')
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
