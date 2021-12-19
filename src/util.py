#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 18:16:14 2021

@author: lovingmage
"""


import random
import resource
import time
import phe.paillier as paillier
from dataclasses import dataclass


#Generate random data point with one-hot-encoding format
def generate_random_data(*args):
    c = sum(args)
    return  [random.randint(0,1) for i in range(c)] 
    
#data = generate_random_data(10,11,12,15)
#print(data)
    

def time_method(method, *args):
    start = time.time()
    method(*args)
    return time.time() - start