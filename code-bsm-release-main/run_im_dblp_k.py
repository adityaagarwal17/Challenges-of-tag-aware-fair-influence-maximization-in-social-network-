from inf_max.algo_im import greedy_im, saturate_im, bsm_tsgreedy_im, bsm_saturate_im, read_file, read_attr, est_inf, calc_obj_vals
from inf_max.imm import IMM

num_nodes, _, graph = read_file("./data/dblp/author-author.csv", is_dir=False)
attrs, groups = read_attr('./data/dblp/countries.csv')
output_file = open('./results/im_results_dblp_countries_k.csv', 'a')
output_file.write('algorithm,k,tau,f,g,time(s)\n')

ks = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
eps = 0.05
tau = 0.8

for k in ks:
    inst_imm = IMM(graph, False, num_nodes, k, 0.25)
    nodes, ris = inst_imm.run()

    sol, time = greedy_im(ris, k, num_nodes)
    dict_inf = est_inf(graph, sol)
    f, g, _ = calc_obj_vals(dict_inf, attrs, groups)
    output_file.write('Greedy,' + str(k) + ',' + 'N/A' + ',' + str(f) + ',' + str(g) + ',' + str(time) + '\n')

    sol, time = saturate_im(ris, nodes, k, num_nodes, attrs, groups)
    dict_inf = est_inf(graph, sol)
    f, g, _ = calc_obj_vals(dict_inf, attrs, groups)
    output_file.write('Saturate,' + str(k) + ',' + 'N/A' + ',' + str(f) + ',' + str(g) + ',' + str(time) + '\n')

    sol, time = bsm_tsgreedy_im(ris, nodes, k, num_nodes, tau, attrs, groups)
    dict_inf = est_inf(graph, sol)
    f, g, _ = calc_obj_vals(dict_inf, attrs, groups)
    output_file.write('BSM-TSGreedy,' + str(k) + ',' + str(tau) + ',' + str(f) + ',' + str(g) + ',' + str(time) + '\n')

    sol, time = bsm_saturate_im(ris, nodes, k, num_nodes, eps, tau, attrs, groups)
    dict_inf = est_inf(graph, sol)
    f, g, _ = calc_obj_vals(dict_inf, attrs, groups)
    output_file.write('BSM-Saturate,' + str(k) + ',' + str(tau) + ',' + str(f) + ',' + str(g) + ',' + str(time) + '\n')

output_file.close()
