from max_cover.algo_mc import greedy_mc, saturate_mc, bsm_tsgreedy_mc, bsm_saturate_mc, read_items, read_attr, calc_obj_vals

items = read_items('./data/pokec/pokec-edges.txt', is_directed=True)
attrs, groups = read_attr('./data/pokec/pokec-attr2.txt')
output_file = open('./results/mc_results_pokec-attr2.csv', 'w')
output_file.write('algorithm,k,tau,f,g,time(s)\n')

ks = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
eps = 0.05
tau = 0.8

for k in ks:
    _, cov, time = greedy_mc(items, k)
    f, g, _ = calc_obj_vals(cov, attrs, groups)
    output_file.write('Greedy,' + str(k) + ',' + 'N/A' + ',' + str(f) + ',' + str(g) + ',' + str(time) + '\n')

    _, cov, time = saturate_mc(items, k, attrs, groups)
    f, g, _ = calc_obj_vals(cov, attrs, groups)
    output_file.write('Saturate,' + str(k) + ',' + 'N/A' + ',' + str(f) + ',' + str(g) + ',' + str(time) + '\n')

    _, cov, time = bsm_tsgreedy_mc(items, k, tau, attrs, groups)
    f, g, _ = calc_obj_vals(cov, attrs, groups)
    output_file.write('BSM-TSGreedy,' + str(k) + ',' + str(tau) + ',' + str(f) + ',' + str(g) + ',' + str(time) + '\n')

    _, cov, time = bsm_saturate_mc(items, k, eps, tau, attrs, groups)
    f, g, _ = calc_obj_vals(cov, attrs, groups)
    output_file.write('BSM-Saturate,' + str(k) + ',' + str(tau) + ',' + str(f) + ',' + str(g) + ',' + str(time) + '\n')

output_file.close()
