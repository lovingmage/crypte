#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 21:32:56 2018

@author: lovingmage
"""
import argparse
import math
import numpy as np
import xxhash
import csv
import time
import seaborn as sns
from sklearn.isotonic import IsotonicRegression  

from matplotlib import pyplot as plt
from matplotlib import rc


# The laplace Mechanism Directly add noise to the query answer
def lapMechanism(trueAns, epsilon, querySensitivity):
    noisyAns = np.zeros(trueAns.shape) 
    noisyAns = trueAns + np.random.laplace(0, querySensitivity/epsilon, trueAns.shape)
    #noisyAns = trueAns + np.random.geometric(1-math.exp(-epsilon), trueAns.shape)
    # print (np.random.laplace(0, querySensitivity/epsilon, trueAns.shape))
    return noisyAns

#Get Data from  Exernal File
def get_data(inputfile):
    D = [];
    with open(str(inputfile)) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        i=0    
        for row in csv_reader:
            D.append(row[0])
            
    return D

#Create Histogram
#@Param: Data -> D,
#@Param: domain lower bound, upperbound -> dom_l, dom_u
#@Param: Total bin number -> bun_num
def creat_bins(D, dom_l, dom_u, bin_num):
    #100 - 0
    dom_range = dom_u - dom_l
    bin_range = dom_range / bin_num
    bin_count = [0 for i in range(bin_num) ]
    #for i in range(0, bin_num, 1):
    #    print (i)
    for i in D:
        bin_count[int(int(i)/bin_range) ] = bin_count[int(int(i)/bin_range)] + 1
    #print (bin_count)
    
    return bin_count
        
# Function Used to Create Noisy CDF
#@Param: e -> epsilon
#@Param: k -> sensitivity 
def compute_noisy_cdf(D, e, k):
    ncdf = []
    for i in range(len(D)):
        ncdf.append(sum(D[1:i+1]))
    cdf_arr = np.asarray(ncdf)
    noisy_cdf = lapMechanism(cdf_arr, e, k)
    
    tmp = np.arange(len(noisy_cdf))
    IRmodel = IsotonicRegression(y_min=0, increasing = True)
    return IRmodel.fit_transform(tmp, noisy_cdf)


#Noisy Filtering
def data_filter(D, nos_cdf, bin_num, bin_range, lo, hi, k):
    D.sort(reverse=False)
    bin_lo_index = int(lo/bin_range)
    bin_hi_index = int(hi/bin_range)
    if bin_lo_index == 0 and bin_hi_index == 0:
        return D[0:(bin_range + 1)]
    if bin_lo_index == 0 and bin_hi_index != 0:
        return D[0: int(nos_cdf[bin_hi_index])]
    else:
        return D[int(nos_cdf[bin_lo_index - k]) : int(nos_cdf[bin_hi_index + k - 1])]
    
# The ground truth range query
def ground_range_query(D, lo, hi):
    counter = 0
    for i in D:
        if int(i) >= lo and int(i) <= hi:
            counter += 1
    return counter
    


# The noisy range query
def noisy_range_query(D, lo, hi, ep):
    counter = 0
    for i in D:
        if int(i) >= lo and int(i) <= hi:
            counter += 1
    counter = counter + np.random.geometric(1-math.exp(- ep))
    return counter
    


#Dispatcher for exp, on attribute age
def dispatch(ep, lo, hi, binNum, binSize, D, p_neb, reps):    
    
    err = np.zeros(reps)
    perf = np.zeros(reps)
    sum_noise = np.zeros(reps)

    for i in range(reps): 
        bc = creat_bins(D, 0, 100, binNum)
        n_cdf = compute_noisy_cdf(bc, ep, 10)
        filtered = data_filter(D, n_cdf, binNum, binSize, lo, hi, p_neb)
        truth_c = ground_range_query(D, lo, hi)
        noisy_c = noisy_range_query(filtered, lo, hi, 0.5) 
        
        err[i] = abs(truth_c - noisy_c)
        perf[i] = len(filtered)/len(D)
        sum_noise[i] = np.random.geometric(1-math.exp(- 0.5))
    
    return np.average(err), np.average(perf), np.average(sum_noise)
    #print (np.average(perf))
    #print ("=====================")



#################
# @Param: epsilon at index
# @Param: bin number
# @Param: query range
# @Param: neighbor bins been included


#err = dispatch(0.01, 20, 30, 20, 5)
#print(err)
    
#ep1 = 0.1
lo = 50
hi = 60
binNum = 50
binSize = 100/binNum
D = get_data("testfile2.txt")

ret_err = []
ret_perf = []
ret_x = []
ret_lperr = []



for i in range(5):
    print (i)
    err, perf, lperr = dispatch(1, lo, hi, binNum, binSize, D, i, 50)
    ret_err.append(err)
    ret_perf.append(perf)
    ret_x.append(2*(i+1))
    ret_lperr.append(lperr)
    
print (ret_err)
print (ret_perf)
    


#exp2
'''
binumlist = [100, 50, 25, 20, 10, 5, 4]

for i in binumlist:
    print (i)
    err, perf, lperr = dispatch(1, lo, hi, i, 100/i, D, 50)
    ret_err.append(err)
    ret_perf.append(perf)
    ret_x = [100, 50, 25, 20, 10, 5, 4]
    ret_lperr.append(lperr)
'''

#exp1 varying ep
'''
for i in range(20):
    print (0.1 + 0.1*i)
    err, perf, lperr = dispatch(0.1 + 0.1*i, lo, hi, binNum, binSize, D, 20)
    ret_err.append(err)
    ret_perf.append(perf)
    ret_ep.append(0.1 + 0.1*i)
    ret_lperr.append(lperr)
'''

plt.figure()
plt.xlabel('Number of Neighboring Bins Included')
plt.ylabel('L1 Norm Error')
plt.plot(ret_x, ret_err, 'r-x', label='NRQ /w Noisy Filtering')
plt.plot(ret_x, ret_lperr, 'b-+', label='NRQ w/o Noisy Filtering')
legend = plt.legend(loc='right top', shadow=False, fontsize='x-large')
plt.show()


plt.figure()
plt.xlabel('Number of Neighboring Bins Included')
plt.ylabel('Performance')
plt.plot(ret_x, ret_perf, 'r-x', label='NRQ /w Noisy Filtering')
#plt.plot(ret_ep, ret_perf, 'b-+', label='NRQ w/o Noisy Filtering')
legend = plt.legend(loc='right top', shadow=False, fontsize='x-large')
plt.show()


plt.figure()
plt.xlabel('L1 Error')
plt.ylabel('Performance')
plt.plot(ret_err, ret_perf, 'r x', label='NRQ /w Noisy Filtering')
#plt.plot(ret_ep, ret_perf, 'b-+', label='NRQ w/o Noisy Filtering')
legend = plt.legend(loc='right top', shadow=False, fontsize='x-large')
plt.show()

