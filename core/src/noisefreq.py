import csv
import time
import numpy as np

from AS import AnalyticsServer
from CSP import CSProvider
from DO import DOwner

import _pickle as cPickle

def evaluate_laplace(inputfile, num_DO, attr, r_start,r_end):
    """
    compute 
    :param inputfile : Data file 
    :param num_DOs: the number of Data Owners
    :param l: the number of attributes per record
    :param attr, v: the objective is to find the count of entries with value v for attribute attr
    :param e: the privacy budget
    :return : return noisy count
    """
    domain_s=[1,1,20,100]
    domain_e=[100,100,40,120]
    D=[[] for i in range(num_DO)]
    #Generate Dataset
    rcount = []
    for i in range(0, 100, 1):
        rcount.append(0)
        
    f = open(inputfile)
    count_tmp = 0
    
    for i in f:
        tmp = int(i.split(',')[attr])
        #print (tmp)
        count_tmp = count_tmp + 1
        if count_tmp <= num_DO:
            rcount[ tmp - 1 ] = rcount[ tmp - 1 ] + 1
        else:
            return rcount
    
'''
clist = evaluate_laplace("testfile.txt",50, 0, 1, 3) 
tmp = 0
for i in range(29):
    tmp = tmp + clist[i]
print (tmp)

print (clist[30])

tmp3 = 0
for i in range(31, 100, 1):
    tmp3 = tmp3 + clist[i]
print (tmp3)
'''
result = np.zeros(10)

x = [[7, 11, 14, 14, 14, 14, 15, 12, 13, 16]]
tmp = 0
for i in range(10):
    result[i] = np.abs(x[0][i] - 14)
    
print (np.mean(result))
print (np.std(result))
    