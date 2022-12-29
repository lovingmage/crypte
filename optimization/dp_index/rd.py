#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 10:59:01 2018

@author: lovingmage
"""

import numpy as np

def dispat(reps):
    for j in range(10):
        err_arr = np.zeros(reps)
        e = 0.1 + 0.2*j
        for i in range(reps):
            u=np.random.geometric(1-pow(2.713,-e))
            v=np.random.geometric(1-pow(2.713,-e))
            z=u-v
            
            u2=np.random.geometric(1-pow(2.713,-e))
            v2=np.random.geometric(1-pow(2.713,-e))
            z2=u2-v2
            
            err_arr[i] = abs(z + z2)
            
        print(np.std(err_arr))
        

dispat(10)            
            
        