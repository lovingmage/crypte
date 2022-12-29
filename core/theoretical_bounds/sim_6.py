#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 09:46:00 2019

@author: lovingmage
"""

import lapmec as lc
import numpy as np


def range_query_err(e=0.1, k=10):
    as_err = lc.gen_laplace(e, k) 
    return abs(as_err)


err_list = []
for i in range(10):
    e = round( (0.1 + i * 0.2), 1)
    e1 = 0.2*e
    e2 = 0.8*e
    
    ind_err = np.zeros(10)
    interval = np.zeros(10)

    err = range_query_err(e, 10)/2
    err_list.append(err)
    log10_err = np.array([1 for i in range(10)]) + err
    #print(err)
    print(err.mean(), err.std(), np.log10(log10_err).mean(), np.log10(log10_err).std())
    
#print(err_list)