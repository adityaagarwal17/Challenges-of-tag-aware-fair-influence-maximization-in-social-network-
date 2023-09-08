import numpy

from facility_loc.algo_fl import calc_obj_vals, read_items, read_users, read_attr, generate_benefit_mat
from facility_loc.algo_fl_opt import fl_ip, bsm_fl_ip, robust_fl_ip

# Experiments on random data
items = read_items('./data/adult-small/adult-features.txt')
users = read_users('./data/adult-small/adult-features.txt')
attrs, groups = read_attr('./data/adult-small/adult-attr2.txt')
output_file = open('results/fl_results_adult_small_optimal.csv', 'w')
output_file.write('algorithm,k,tau,f,g,time(s)\n')

k = 5

bmat = generate_benefit_mat(items, users)

sol, time = fl_ip(bmat, k)
f, g, _ = calc_obj_vals(bmat, sol, attrs, groups)
output_file.write('OPT_f,' + str(k) + ',' + 'N/A' + ',' + str(f) + ',' + str(g) + ',' + str(time) + '\n')

sol, time = robust_fl_ip(bmat, k, attrs, groups)
f, g, _ = calc_obj_vals(bmat, sol, attrs, groups)
output_file.write('OPT_g,' + str(k) + ',' + 'N/A' + ',' + str(f) + ',' + str(g) + ',' + str(time) + '\n')

opt_g = g

taus = numpy.arange(0.1, 1.0, 0.1)

for tau in taus:
    sol, time = bsm_fl_ip(bmat, k, tau, opt_g, attrs, groups)
    f, g, _ = calc_obj_vals(bmat, sol, attrs, groups)
    output_file.write('BSM-Optimal,' + str(k) + ',' + str(tau) + ',' + str(f) + ',' + str(g) + ',' + str(time) + '\n')

output_file.close()
