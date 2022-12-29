#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 12:18:50 2018

@author: lovingmage
"""

import csv
import time
import numpy as np
import math
from AS import AnalyticsServer
from CSP import CSProvider
from DO import DOwner
from sklearn.metrics import f1_score

import _pickle as cPickle


def evaluate_hvhitter(inputfile, num_DO, attr,r_start, r_end,e):
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
    domain_e=[2,100,40,120]
    domain_size=[2,100,20,20]
    runs=20
    l=2
    D=[[] for i in range(num_DO)]
    #Generate Dataset


    with open(str(inputfile)) as csv_file:
     csv_reader = csv.reader(csv_file, delimiter=',')
     line_count = 0
     i=0    
     for row in csv_reader:
        if(line_count<num_DO):
           D[line_count]=row
           line_count=line_count+1
        else:
           break
       

    '''Start Secure protocol computation'''
    n_length=2048
	

    # declare CSP & MLE & DOwners
    csp = CSProvider()
    As = AnalyticsServer()
    #As = cPickle.load(open("./5000-as.pkl","rb")) 
    DOwners = []
    for index in range(num_DO):
        DOwners.append(DOwner(D[index],domain_s,domain_e))

    print('Phase 1 : Protocol Laplace-DO')  
    # declare Crypto Service Provider(CSP) & Phase1 step1
    start_P11 = time.time()
    csp.key_gen(n_length)
    end_P11 = time.time()

    # publish public_key to AS & Downers
    As.set_PK(csp.get_MPK())
    for d_owner in DOwners:
        d_owner.set_MPK(csp.get_MPK())    

    # Phase1 step2
    start_P12 = time.time()     
    for d_owner in DOwners:
        d_owner.computeEnc_X()
    end_P12 = time.time()

    # Phase2 Step 1
    print('Phase 2 : Protocol RangeQueries-AS')
    start_P21 = time.time()
    for d_owner in DOwners:
        enc_Xi = d_owner.getEnc_X()
        #as merges enc_Xi
        As.add_enc_X(enc_Xi,num_DO)
    end_P21 = time.time()
    
    print ('Export As Encrypted Data...')
    cPickle.dump(As,open("./5000-As.pkl","wb"))
    cPickle.dump(csp,open("./5000-csp.pkl","wb"))

    # Phase2 step2
    start_P22 = time.time()
    T1 = As.Projection(attr)
    C = As.generateEncCount_GroupBy(T1)
    end_P22 = time.time()
    
    start_P23 = time.time()
    ans_ind = np.argsort(csp.decryptonly(C))
    ans_ind = ans_ind[0 : 5]
    print(ans_ind)
    print("xxxxx")
    
        
    print('Answer : Protocol Laplace for e =', e)
    end_P23 = time.time()
    
    #end_P31 = time.time()

    print('Runtime(KeyGen) = ', end_P11 - start_P11)
    print('Runtime(DO_ComputeEncX) = ', (end_P12 - start_P12)/num_DO )
    print('Runtime(AS_MergeEncX) = ', end_P21 - start_P21)
    print('Runtime(AS_Laplace) = ', end_P22 - start_P22)
    print('Runtime(CSP_Laplace) = ', end_P23 - start_P23)

'''
    for i in range(10):
        results = np.zeros(runs)
        for j in range(runs):
            C = As.generateEncNoisyCount_GroupBy(T1, 0.1 + 0.2*i)
            tmp = np.argsort(csp.decryptonly(C))
            tmp = tmp[0 : 5]
            results[j] = f1_score(ans_ind, tmp, average='macro')
        print(np.average(results))
        print(np.std(results))
        print ("       ")
    '''
            


   # compute Runtime
