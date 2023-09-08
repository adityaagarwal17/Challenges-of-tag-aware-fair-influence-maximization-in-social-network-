from facility_loc.algo_fl_indiv import greedy_fl_indiv, saturate_fl_indiv, bsm_tsgreedy_fl_indiv, bsm_saturate_fl_indiv, calc_obj_vals, read_items, read_users, generate_benefit_mat

items = read_items('data/foursquare/nyc-items.txt')
users = read_users('data/foursquare/nyc-users.txt')
output_file = open('./results/fl_results_nyc.csv', 'a')
output_file.write('algorithm,k,tau,f,g,time(s)\n')

ks = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
eps = 0.05
tau = 0.8

for k in ks:
    bmat = generate_benefit_mat(items, users)

    sol, time = greedy_fl_indiv(bmat, k)
    f, g = calc_obj_vals(bmat, sol)
    output_file.write('Greedy,' + str(k) + ',' + 'N/A' + ',' + str(f) + ',' + str(g) + ',' + str(time) + '\n')

    sol, time = saturate_fl_indiv(bmat, k)
    f, g = calc_obj_vals(bmat, sol)
    output_file.write('Saturate,' + str(k) + ',' + 'N/A' + ',' + str(f) + ',' + str(g) + ',' + str(time) + '\n')

    total_time = 0
    for r in range(10):
        sol, time = bsm_tsgreedy_fl_indiv(bmat, k, tau)
        f, g = calc_obj_vals(bmat, sol)
        total_time += time
    output_file.write('BSM-TSGreedy,' + str(k) + ',' + str(tau) + ',' + str(f) + ',' + str(g) + ',' + str(total_time / 10) + '\n')

    total_time = 0
    for r in range(10):
        sol, time = bsm_saturate_fl_indiv(bmat, k, eps, tau)
        f, g = calc_obj_vals(bmat, sol)
        total_time += time
    output_file.write('BSM-Saturate,' + str(k) + ',' + str(tau) + ',' + str(f) + ',' + str(g) + ',' + str(total_time / 10) + '\n')

output_file.close()
