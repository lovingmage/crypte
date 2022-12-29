#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 17:32:29 2019

@author: lovingmage
"""

import random
import numpy as np
import math

cnt_50 = 10
cnt_51_52 = 14
cnt_53_60 = 21
total_cnt_60_60 = 45

for i in range(10):
    e = (0.15 + i * 0.2)/math.log(100)
    z = np.zeros(10)
    for k in range(10):
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
        ncnt_total = ncnt_50 + ncnt_51_52 + ncnt_53_60  + u4 - v4
        err = abs(total_cnt_60_60 - ncnt_total)
        z[k] = err
        
        
    print(z.mean())
    print(z.std())
    print(" ")
    

