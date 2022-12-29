#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 26 17:18:15 2019

@author: lovingmage
"""
import lapmec as lc
import numpy as np

def sim_p1_range_tree():
    cnt_50 = 10
    cnt_51_52 = 14
    cnt_53_60 = 21
    total_cnt_60_60 = 45
    
    for i in range(10):
        e = (0.15 + i * 0.2)/math.log(100)
        z = np.zeros(5)
        for k in range(5):
            u1=np.random.geometric(1-math.exp(-e))
            v1=np.random.geometric(1-math.exp(-e))
            ncnt_50 = cnt_50 + u1 - v1
            
            u2=np.random.geometric(1-math.exp(-e))
            v2=np.random.geometric(1-math.exp(-e))
            ncnt_51_52 = cnt_51_52 + u2 - v2
            
            u3=np.random.geometric(1-math.exp(-e))
            v3=np.random.geometric(1-math.exp(-e))
            ncnt_53_60 = cnt_53_60 + u3 - v3
            
            u4=np.random.geometric(1-math.exp(-e))
            v4=np.random.geometric(1-math.exp(-e))
            # Remove the following noise, mimic the cdp mode
            ncnt_total = ncnt_50 + ncnt_51_52 + ncnt_53_60
            err = abs(total_cnt_60_60 - ncnt_total)
            z[k] = err
            
        log10z = np.log10(z)
        print(z.mean(), z.std(), log10z.mean(), log10z.std())
        print(" ")

#ratio = {'0.1':3.675883329, '0.3':4.01083045, '0.5':3.762405913, '0.7':3.998949862, '0.9':3.768185074, '1.1':3.994747241, '1.3':4.216370214, '1.5': 4.03469213, '1.7': 3.701322031, '1.9': 3.346989949}

def range_query_err(e=0.1, k=10):
    as_err = lc.gen_laplace(e, k) 
    return abs(as_err)

def sim_p1():
    err_list = []
    for i in range(10):
        e = round( (0.1 + i * 0.2), 1)
    
        err = range_query_err(e).astype(int)
        err_list.append(err)
        log10_err = np.array([1 for i in range(10)]) + err
        #print(err)
        print(err.mean(), err.std(), np.log10(log10_err).mean(), np.log10(log10_err).std())
        
    #print(err_list)
    
sim_p1_range_tree()
