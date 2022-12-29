#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 22:34:01 2018

@author: lovingmage
"""
from sklearn.metrics import f1_score
import numpy as np
import math
    
def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3 

def avg_f1(file, e):

    true_count_list =[]
    f = open(file)
    
    for i in f:
        true_count_list.append(int(i))
        
    noise_count_list = []
    u=np.random.geometric(1-math.exp(-e), size=len(true_count_list))
    v=np.random.geometric(1-math.exp(-e), size=len(true_count_list))
    z=u-v
    noise_count_list = true_count_list + z
    
    
    noise_index = sorted(range(len(noise_count_list)), key=lambda i: noise_count_list[i])[-10:]
    true_index = sorted(range(len(true_count_list)), key=lambda i: true_count_list[i])[-10:]
    
    
    #print (noise_index)
    #print (true_index)
    
    precision = len(intersection(noise_index, true_index)) / len(noise_index)
    recall = len(intersection(noise_index, true_index)) / len(noise_index)
    return 2*precision*recall/(precision + recall) 
        
'''
ep = [0.1, 0.3, 0.5, 0.7, 0.9]
for j in ep:
    print ("Epsilon round ", j)
    tmp = []
    for i in range(1, 100, 1):
        tmp.append(avg_f1("adult100.txt", j))
    x = np.array(tmp)
    print (np.mean(x))
    print (np.std(x))
    
'''
e = 0.9
distinct = 0
f = open("adult100.txt")
for i in f:
    if int(i) == 1:
        continue
    else:
        distinct = distinct + 1
results = np.zeros(10)
for i in range(10):
    u=np.random.geometric(1-math.exp(-e), 1)
    v=np.random.geometric(1-math.exp(-e), 1)
    z=int(u-v)
    results[i] = np.abs( (distinct + z) - distinct)

print (np.mean(results))
print (np.std(results))