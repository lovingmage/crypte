#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 26 21:25:59 2019

@author: lovingmage
"""

import lapmec as lc
import numpy as np

import lapmec as lc
import numpy as np

def range_query_err(e=0.1, k=10):
    as_err = lc.gen_laplace(e, k) 
    return abs(as_err/2)
    
def get_true_hist(file):
   TH = lc.read_data_to_hist(file)
   return TH

TH = get_true_hist("uci_adult_sorted.txt")
print(TH)

err_list = []
for i in range(10):
    e = round( (0.1 + i * 0.2), 1)

    err = range_query_err(e/2).astype(int)
    err_list.append(err)
    log10_err = np.array([1 for i in range(10)]) + err
    #print(err)
    #print(err.mean(), err.std(), np.log10(log10_err).mean(), np.log10(log10_err).std())
    print(err.mean(), err.std())
print(err_list)