import numpy

from max_cover.algo_mc import greedy_mc, saturate_mc, smsc_mc, bsm_tsgreedy_mc, bsm_saturate_mc, read_items, read_attr, calc_obj_vals

# Experiments on random graphs
items = read_items('./data/facebook/facebook-edges.txt', is_directed=False)
attrs, groups = read_attr('./data/facebook/facebook-attr1.txt')
output_file = open('./results/mc_results_facebook_attr1_tau.csv', 'w')
output_file.write('algorithm,k,tau,f,g,time(s)\n')

k = 5
eps = 0.05

_, cov, time = greedy_mc(items, k)
f, g, _ = calc_obj_vals(cov, attrs, groups)
output_file.write('Greedy,' + str(k) + ',' + 'N/A' + ',' + str(f) + ',' + str(g) + ',' + str(time) + '\n')

_, cov, time = saturate_mc(items, k, attrs, groups)
f, g, _ = calc_obj_vals(cov, attrs, groups)
output_file.write('Saturate,' + str(k) + ',' + 'N/A' + ',' + str(f) + ',' + str(g) + ',' + str(time) + '\n')

taus = numpy.arange(0.1, 1.0, 0.1)

for tau in taus:
    total_time = 0
    for r in range(10):
        _, cov, time = smsc_mc(items, k, tau, attrs, groups)
        total_time += time
        f, g, _ = calc_obj_vals(cov, attrs, groups)
    output_file.write('SMSC,' + str(k) + ',' + str(tau) + ',' + str(f) + ',' + str(g) + ',' + str(total_time / 10) + '\n')

for tau in taus:
    total_time = 0
    for r in range(10):
        _, cov, time = bsm_tsgreedy_mc(items, k, tau, attrs, groups)
        total_time += time
    f, g, _ = calc_obj_vals(cov, attrs, groups)
    output_file.write('BSM-TSGreedy,' + str(k) + ',' + str(tau) + ',' + str(f) + ',' + str(g) + ',' + str(total_time / 10) + '\n')

for tau in taus:
    total_time = 0
    for r in range(10):
        _, cov, time = bsm_saturate_mc(items, k, eps, tau, attrs, groups)
        total_time += time
    f, g, _ = calc_obj_vals(cov, attrs, groups)
    output_file.write('BSM-Saturate,' + str(k) + ',' + str(tau) + ',' + str(f) + ',' + str(g) + ',' + str(total_time / 10) + '\n')

items.clear()
attrs.clear()
groups.clear()
output_file.close()

items = read_items('./data/facebook/facebook-edges.txt', is_directed=False)
attrs, groups = read_attr('./data/facebook/facebook-attr2.txt')
output_file = open('./results/mc_results_facebook_attr2_tau.csv', 'w')
output_file.write('algorithm,k,tau,f,g,time(s)\n')

_, cov, time = greedy_mc(items, k)
f, g, _ = calc_obj_vals(cov, attrs, groups)
output_file.write('Greedy,' + str(k) + ',' + 'N/A' + ',' + str(f) + ',' + str(g) + ',' + str(time) + '\n')

_, cov, time = saturate_mc(items, k, attrs, groups)
f, g, _ = calc_obj_vals(cov, attrs, groups)
output_file.write('Saturate,' + str(k) + ',' + 'N/A' + ',' + str(f) + ',' + str(g) + ',' + str(time) + '\n')

taus = numpy.arange(0.1, 1.0, 0.1)

for tau in taus:
    total_time = 0
    for r in range(10):
        _, cov, time = bsm_tsgreedy_mc(items, k, tau, attrs, groups)
        total_time += time
    f, g, _ = calc_obj_vals(cov, attrs, groups)
    output_file.write('BSM-TSGreedy,' + str(k) + ',' + str(tau) + ',' + str(f) + ',' + str(g) + ',' + str(total_time / 10) + '\n')

for tau in taus:
    total_time = 0
    for r in range(10):
        _, cov, time = bsm_saturate_mc(items, k, eps, tau, attrs, groups)
        total_time += time
    f, g, _ = calc_obj_vals(cov, attrs, groups)
    output_file.write('BSM-Saturate,' + str(k) + ',' + str(tau) + ',' + str(f) + ',' + str(g) + ',' + str(total_time / 10) + '\n')

output_file.close()
