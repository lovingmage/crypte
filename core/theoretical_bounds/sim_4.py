#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 09:29:07 2019

@author: lovingmage
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 26 20:10:23 2019

@author: lovingmage
"""

import lapmec as lc
import numpy as np

def generate_index_noise(bin_size, bin_number, file, mode = "na", e=0.1):
    D = lc.read_data_to_hist(file, mode=mode)
    n_cdf = lc.index_noisy_cdf(D, bin_size, bin_number, e)
    interval = n_cdf[5] - n_cdf[4]
    noise = n_cdf[4] - 30641
    
    return interval, noise

def gen_index_noise_arr(bin_size, bin_number, file, arr_k = 10, mode = "na", e=0.1):
    noise = np.zeros(arr_k)
    interval = np.zeros(arr_k)
    for i in range(arr_k):
        interval[i], noise[i] = generate_index_noise(bin_size, bin_number, file, mode=mode, e=e)
    return interval, noise

def range_query_err(e=0.1, k=10):
    as_err = lc.gen_laplace(e, k) 
    return abs(as_err)

def marginal_on_age(e=0.1):
    mal_err = np.zeros(10)
    for i in range(200):
        mal_err += range_query_err(e).astype(int)
    return mal_err

def cdp_marginal_on_age(e=0.1):
    mal_err = np.zeros(10)
    for i in range(200):
        mal_err += abs(lc.gen_laplace_once(e, 10)).astype(int)
    return mal_err

    
err_list = []
for i in range(10):
    e = round( (0.1 + i * 0.2), 1)
    e1 = 0.2*e
    e2 = 0.8*e
    
    ind_err = np.zeros(10)
    interval = np.zeros(10)
    interval, ind_err = gen_index_noise_arr(4, 10, "uci_adult_sorted.txt", 10, "na", e1)

    #err = marginal_on_age(e2/2) - ind_err
    err = cdp_marginal_on_age(e2/2)
    err_list.append(err)
    log10_err = np.array([1 for i in range(10)]) + err
    #print(err)
    print(err.mean(), err.std(), np.log10(log10_err).mean(), np.log10(log10_err).std())
    
#print(err_list)