import numpy

from facility_loc.algo_fl import greedy_fl, saturate_fl, smsc_fl, bsm_tsgreedy_fl, bsm_saturate_fl, calc_obj_vals, read_items, read_users, read_attr, generate_benefit_mat

# Experiments on random data
items = read_items('C:/Users/hp/Downloads/code-bsm-release-main/data/rand_data/rand_c2_features.txt')
users = read_users('C:/Users/hp/Downloads/code-bsm-release-main/data/rand_data/rand_c2_features.txt')
attrs, groups = read_attr('C:/Users/hp/Downloads/code-bsm-release-main/data/rand_data/rand_c2_attr.txt')
output_file = open('C:/Users/hp/Downloads/code-bsm-release-main/fl_results_rand_c2.csv', 'w')
output_file.write('algorithm,k,tau,f,g,time(s)\n')

k = 5
eps = 0.05

bmat = generate_benefit_mat(items, users)

sol, time = greedy_fl(bmat, k)
f, g, _ = calc_obj_vals(bmat, sol, attrs, groups)
output_file.write('Greedy,' + str(k) + ',' + 'N/A' + ',' + str(f) + ',' + str(g) + ',' + str(time) + '\n')

sol, time = saturate_fl(bmat, k, attrs, groups)
f, g, _ = calc_obj_vals(bmat, sol, attrs, groups)
output_file.write('Saturate,' + str(k) + ',' + 'N/A' + ',' + str(f) + ',' + str(g) + ',' + str(time) + '\n')

taus = numpy.arange(0.1, 1.0, 0.1)

for tau in taus:
    total_time = 0
    for r in range(10):
        sol, time = smsc_fl(bmat, k, tau, attrs, groups)
        total_time += time
    f, g, _ = calc_obj_vals(bmat, sol, attrs, groups)
    output_file.write('SMSC,' + str(k) + ',' + str(tau) + ',' + str(f) + ',' + str(g) + ',' + str(total_time / 10) + '\n')

for tau in taus:
    total_time = 0
    for r in range(10):
        sol, time = bsm_tsgreedy_fl(bmat, k, tau, attrs, groups)
        total_time += time
    f, g, _ = calc_obj_vals(bmat, sol, attrs, groups)
    output_file.write('BSM-TSGreedy,' + str(k) + ',' + str(tau) + ',' + str(f) + ',' + str(g) + ',' + str(total_time / 10) + '\n')

for tau in taus:
    total_time = 0
    for r in range(10):
        sol, time = bsm_saturate_fl(bmat, k, eps, tau, attrs, groups)
        total_time += time
    f, g, _ = calc_obj_vals(bmat, sol, attrs, groups)
    output_file.write('BSM-Saturate,' + str(k) + ',' + str(tau) + ',' + str(f) + ',' + str(g) + ',' + str(total_time / 10) + '\n')

output_file.close()

items = read_items('C:/Users/hp/Downloads/code-bsm-release-main/data/rand_data/rand_c3_features.txt')
users = read_users('C:/Users/hp/Downloads/code-bsm-release-main/data/rand_data/rand_c3_features.txt')
attrs, groups = read_attr('C:/Users/hp/Downloads/code-bsm-release-main/data/rand_data/rand_c3_attr.txt')
output_file = open('C:/Users/hp/Downloads/code-bsm-release-main/fl_results_rand_c3.csv', 'w')
output_file.write('algorithm,k,tau,f,g,time(s)\n')

bmat = generate_benefit_mat(items, users)

sol, time = greedy_fl(bmat, k)
f, g, _ = calc_obj_vals(bmat, sol, attrs, groups)
output_file.write('Greedy,' + str(k) + ',' + 'N/A' + ',' + str(f) + ',' + str(g) + ',' + str(time) + '\n')

sol, time = saturate_fl(bmat, k, attrs, groups)
f, g, _ = calc_obj_vals(bmat, sol, attrs, groups)
output_file.write('Saturate,' + str(k) + ',' + 'N/A' + ',' + str(f) + ',' + str(g) + ',' + str(time) + '\n')

taus = numpy.arange(0.1, 1.0, 0.1)

for tau in taus:
    total_time = 0
    for r in range(10):
        sol, time = bsm_tsgreedy_fl(bmat, k, tau, attrs, groups)
        total_time += time
    f, g, _ = calc_obj_vals(bmat, sol, attrs, groups)
    output_file.write('BSM-TSGreedy,' + str(k) + ',' + str(tau) + ',' + str(f) + ',' + str(g) + ',' + str(total_time / 10) + '\n')

for tau in taus:
    total_time = 0
    for r in range(10):
        sol, time = bsm_saturate_fl(bmat, k, eps, tau, attrs, groups)
        total_time += time
    f, g, _ = calc_obj_vals(bmat, sol, attrs, groups)
    output_file.write('BSM-Saturate,' + str(k) + ',' + str(tau) + ',' + str(f) + ',' + str(g) + ',' + str(total_time / 10) + '\n')

output_file.close()
