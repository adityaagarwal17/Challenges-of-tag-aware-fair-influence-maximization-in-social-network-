from max_cover.algo_mc import greedy_mc, saturate_mc, smsc_mc, bsm_tsgreedy_mc, bsm_saturate_mc, read_items, read_attr, calc_obj_vals

items = read_items('./data/facebook/facebook-edges.txt', is_directed=False)
attrs, groups = read_attr('./data/facebook/facebook-attr1.txt')
output_file = open('./results/mc_results_facebook-attr1.csv', 'a')
output_file.write('algorithm,k,tau,f,g,time(s)\n')

ks = [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
eps = 0.05
tau = 0.8

for k in ks:
    _, cov, time = greedy_mc(items, k)
    f, g, _ = calc_obj_vals(cov, attrs, groups)
    output_file.write('Greedy,' + str(k) + ',' + 'N/A' + ',' + str(f) + ',' + str(g) + ',' + str(time) + '\n')

    _, cov, time = saturate_mc(items, k, attrs, groups)
    f, g, _ = calc_obj_vals(cov, attrs, groups)
    output_file.write('Saturate,' + str(k) + ',' + 'N/A' + ',' + str(f) + ',' + str(g) + ',' + str(time) + '\n')

    total_time = 0
    for r in range(10):
        _, cov, time = smsc_mc(items, k, tau, attrs, groups)
        f, g, _ = calc_obj_vals(cov, attrs, groups)
        total_time += time
    output_file.write('SMSC,' + str(k) + ',' + str(tau) + ',' + str(f) + ',' + str(g) + ',' + str(total_time / 10) + '\n')

    total_time = 0
    for r in range(10):
        _, cov, time = bsm_tsgreedy_mc(items, k, tau, attrs, groups)
        f, g, _ = calc_obj_vals(cov, attrs, groups)
        total_time += time
    output_file.write('BSM-TSGreedy,' + str(k) + ',' + str(tau) + ',' + str(f) + ',' + str(g) + ',' + str(total_time / 10) + '\n')

    total_time = 0
    for r in range(10):
        _, cov, time = bsm_saturate_mc(items, k, eps, tau, attrs, groups)
        f, g, _ = calc_obj_vals(cov, attrs, groups)
        total_time += time
    output_file.write('BSM-Saturate,' + str(k) + ',' + str(tau) + ',' + str(f) + ',' + str(g) + ',' + str(total_time / 10) + '\n')

output_file.close()
