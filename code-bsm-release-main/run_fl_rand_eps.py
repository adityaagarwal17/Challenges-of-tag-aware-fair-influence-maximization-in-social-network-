import numpy

from facility_loc.algo_fl import bsm_saturate_fl, calc_obj_vals, read_items, read_users, read_attr, generate_benefit_mat

# Experiments on random data
items = read_items('C:/Users/hp/Downloads/code-bsm-release-main/data/rand_data/rand_c2_features.txt')
users = read_users('C:/Users/hp/Downloads/code-bsm-release-main/data/rand_data/rand_c2_features.txt')
attrs, groups = read_attr('C:/Users/hp/Downloads/code-bsm-release-main/data/rand_data/rand_c2_attr.txt')
output_file = open('C:/Users/hp/Downloads/code-bsm-release-main/fl_results_rand_c2_eps.csv', 'w')
output_file.write('algorithm,k,eps,f,g,time(s)\n')
k = 5
tau = 0.8
bmat = generate_benefit_mat(items, users)

eps_vals = numpy.arange(0.01, 1.0, 0.01)

for eps in eps_vals:
    sol, time = bsm_saturate_fl(bmat, k, eps, tau, attrs, groups)
    f, g, _ = calc_obj_vals(bmat, sol, attrs, groups)
    output_file.write('BSM-Saturate,' + str(k) + ',' + str(eps) + ',' + str(f) + ',' + str(g) + ',' + '-' + '\n')

output_file.close()

items = read_items('C:/Users/hp/Downloads/code-bsm-release-main/data/rand_data/rand_c3_features.txt')
users = read_users('C:/Users/hp/Downloads/code-bsm-release-main/data/rand_data/rand_c3_features.txt')
attrs, groups = read_attr('C:/Users/hp/Downloads/code-bsm-release-main/data/rand_data/rand_c3_attr.txt')
output_file = open('C:/Users/hp/Downloads/code-bsm-release-main/fl_results_rand_c3_eps.csv', 'w')
output_file.write('algorithm,k,eps,f,g,time(s)\n')

bmat = generate_benefit_mat(items, users)

for eps in eps_vals:
    sol, time = bsm_saturate_fl(bmat, k, eps, tau, attrs, groups)
    f, g, _ = calc_obj_vals(bmat, sol, attrs, groups)
    output_file.write('BSM-Saturate,' + str(k) + ',' + str(eps) + ',' + str(f) + ',' + str(g) + ',' + '-' + '\n')

output_file.close()

print(" yeahhhhhhhhhhhhhhhh finalllllly done")