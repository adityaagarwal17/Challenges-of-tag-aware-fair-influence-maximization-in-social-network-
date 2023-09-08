from facility_loc.algo_fl import greedy_fl, saturate_fl, bsm_tsgreedy_fl, bsm_saturate_fl, calc_obj_vals, read_items, read_users, read_attr, generate_benefit_mat


items = read_items('C:/Users/hp/Downloads/code-bsm-release-main/data/adult/adult-features.txt')
users = read_users('C:/Users/hp/Downloads/code-bsm-release-main/data/adult/adult-features.txt')
attrs, groups = read_attr('C:/Users/hp/Downloads/code-bsm-release-main/data/adult/adult-attr2.txt')
output_file = open('C:/Users/hp/Downloads/code-bsm-release-main/fl_results_adult-attr2.csv', 'a')
output_file.write('algorithm,k,tau,f,g,time(s)\n')

ks = [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
eps = 0.05
tau = 0.8

for k in ks:
    bmat = generate_benefit_mat(items, users)

    sol, time = greedy_fl(bmat, k)
    f, g, _ = calc_obj_vals(bmat, sol, attrs, groups)
    output_file.write('Greedy,' + str(k) + ',' + 'N/A' + ',' + str(f) + ',' + str(g) + ',' + str(time) + '\n')

    sol, time = saturate_fl(bmat, k, attrs, groups)
    f, g, _ = calc_obj_vals(bmat, sol, attrs, groups)
    output_file.write('Saturate,' + str(k) + ',' + 'N/A' + ',' + str(f) + ',' + str(g) + ',' + str(time) + '\n')

    total_time = 0
    for r in range(10):
        sol, time = bsm_tsgreedy_fl(bmat, k, tau, attrs, groups)
        f, g, _ = calc_obj_vals(bmat, sol, attrs, groups)
        total_time += time
    output_file.write('BSM-TSGreedy,' + str(k) + ',' + str(tau) + ',' + str(f) + ',' + str(g) + ',' + str(total_time / 10) + '\n')

    total_time = 0
    for r in range(10):
        sol, time = bsm_saturate_fl(bmat, k, eps, tau, attrs, groups)
        f, g, _ = calc_obj_vals(bmat, sol, attrs, groups)
        total_time += time
    output_file.write('BSM-Saturate,' + str(k) + ',' + str(tau) + ',' + str(f) + ',' + str(g) + ',' + str(total_time / 10) + '\n')

output_file.close()

print(" yeahhhhhhhhhhhhhhhh finalllllly done")