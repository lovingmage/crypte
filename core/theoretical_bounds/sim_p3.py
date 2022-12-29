#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 26 20:10:23 2019

@author: lovingmage
"""

import lapmec as lc
import numpy as np

def range_query_err(e=0.1, k=10):
    as_err = lc.gen_laplace_once(e, k) 
    return abs(as_err)

def marginal_on_age(e=0.1):
    mal_err = np.zeros(10)
    for i in range(200):
        mal_err += range_query_err(e).astype(int)
    return mal_err
    
err_list = []
for i in range(10):
    e = round( (0.15 + i * 0.2), 1)

    err = marginal_on_age(e/2)
    err_list.append(err)
    log10_err = np.array([1 for i in range(10)]) + err
    #print(err)
    print(err.mean(), err.std(), np.log10(log10_err).mean(), np.log10(log10_err).std())
    
print(err_list)
    