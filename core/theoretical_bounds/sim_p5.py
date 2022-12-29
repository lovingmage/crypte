#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 27 13:14:06 2019

@author: lovingmage
"""
import lapmec as lc
import numpy as np

#Generate missing records via true idx and noisy idx
def get_index_err(idx_lo_t, idx_hi_t, idx_lo_n, idx_hi_n):
    lo_err = idx_lo_t - idx_lo_n
    hi_err = idx_hi_t - idx_hi_n
    
    if lo_err > 0:
        lo_err = 0
        
    if hi_err < 0:
        hi_err = 0
    
    #print(lo_err + hi_err)
    return lo_err + hi_err
    
    

def generate_index_noise(bin_size, bin_number, file, mode = "na", e=0.1):
    D = lc.read_data_to_hist(file, mode=mode)
    n_cdf = lc.index_noisy_cdf(D, bin_size, bin_number, e)

    t_idx_lo = sum(D[1:21])
    t_idx_hi = sum(D[1:22])
    #print(true_idx_hi - true_idx_lo)
    cdf = lc.index_noisy_cdf(D, bin_size, bin_number)
    interval = n_cdf[9] - n_cdf[0]
    
    #noise = n_cdf[4] - cdf[4]
    noise = get_index_err(t_idx_lo, t_idx_hi, n_cdf[0], n_cdf[9])
    #print(noise)
    #print("======\n\n")

    
    return interval, noise

def gen_index_noise_arr(bin_size, bin_number, file, arr_k = 10, mode = "na", e=0.1):
    noise = np.zeros(arr_k)
    interval = np.zeros(arr_k)
    for i in range(arr_k):
        interval[i], noise[i] = generate_index_noise(bin_size, bin_number, file, mode=mode, e=e)
    return interval, noise
      

def simulate_index_ep_perf():
    for i in range(9):
            e1 = (0.11 + i * 0.11)
            e2 = 1.1 - e1
            ind_err = np.zeros(10)
            interval = np.zeros(10)
            interval, ind_err = gen_index_noise_arr(4, 10, "uci_adult_sorted.txt", 10, "na", e1)
            
            for i in range(10):
                if ind_err[i] < 0:
                    ind_err[i] = 0
                else:
                    # Need to re-write this is the restriction of age=30 which consists 7.5% of whole dataset
                    ind_err[i] = int(ind_err[i] * 0.075)
            
                    
            lap_err = np.zeros(10)
            lap_err = gen_laplace(e2, 10)
            
            norm_err = abs(lap_err - ind_err)
            final_err = norm_err/1.36
            #print(norm_err.mean(), norm_err.std(), final_err.mean(), final_err.std())

            interval = 32561/interval
            print(norm_err.mean(), norm_err.std(), final_err.mean(), final_err.std(), interval.mean(), interval.std())
            #print(interval.mean(), interval.std())
            
simulate_index_ep_perf()
            
'''
for i in range(10):
    e = (0.1 + i * 0.2)
    e1 = 0.2*e
    e2 = 1*e
    ind_err = np.zeros(10)
    ind_err = lc.gen_index_noise(e1, 10, 10)
    interval = np.zeros(10)
    interval, ind_err = gen_index_noise_arr(4, 10, "uci_adult_sorted.txt", 10, "na", e1)
    for i in range(10):
                if ind_err[i] < 0:
                    ind_err[i] = 0
                else:
                    ind_err[i] = int(ind_err[i] * 0.075)
                    
    lap_err = np.zeros(10)
    lap_err = lc.gen_laplace(e2, 10) / 2
            
    final_err = abs(lap_err)
    log_results = lc.convert_to_log_err(final_err)
    print(final_err.mean(), final_err.std(), log_results.mean(),log_results.std())
'''