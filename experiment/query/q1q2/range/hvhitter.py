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

def precision(ref, predicted):
    tp = 0.0
    fp = 0.0
    for i in ref:
        if i in predicted:
            tp = tp + 1
    for j in predicted:
        if j not in ref:
            fp = fp + 1
    if (tp + fp) == 0.0:
        return 0.0
    
    return tp/(tp + fp)

def recall(ref, predicted):
    fn = 0.0
    tp = 0.0
    for i in ref:
        if i in predicted:
            tp = tp + 1
    return tp/len(ref)

def f1Score(pre, rec):
    tmp1 = 2 * pre * rec
    tmp2 = pre + rec
    
    if tmp2 == 0.0:
        return 0.0
    return tmp1/tmp2

def err_measure(ref, predicted, histogram_t, delta, e):
    sum_cnt = 0
    slack = (1/e) * math.log(1/delta)
    #print (slack)
    #print (histogram_t)
    for j in predicted:
        if (j not in ref):
            sum_cnt += 1
            
    return (len(ref) - sum_cnt)/len(ref)
        

def evaluate_hvhitter(inputfile, num_DO, attr,r_start, r_end, e):
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

    #print('Phase 1 : Protocol Laplace-DO')  
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
    #print('Phase 2 : Protocol RangeQueries-AS')
    start_P21 = time.time()
    for d_owner in DOwners:
        enc_Xi = d_owner.getEnc_X()
        #as merges enc_Xi
        As.add_enc_X(enc_Xi,num_DO)
    end_P21 = time.time()
    
    #print ('Export As Encrypted Data...')
    #cPickle.dump(As,open("./5000-As.pkl","wb"))
    #cPickle.dump(csp,open("./5000-csp.pkl","wb"))

    # Phase2 step2
    start_P22 = time.time()
    As.range_tree(attr)
    size=domain_e[attr]-domain_s[attr]+1
    k=math.ceil(math.log(size,2))
    As.construct_noisyRangeTree(e/k)
    end_P22= time.time()
    
    histogram_t = np.zeros(100)
    histogram_n = np.zeros(100)
    
    start_P23 = time.time()
    for i in range(100):
        c1,c2=As.range_q(i,i+1)
        tp1 = time.time()
        c1+c2
        tp2 = time.time()
        ans_n=csp.Laplace([c2],e/k,1)
        ans_t=csp.decryptonly([c1])
        histogram_t[i] = int(ans_t[0])
        histogram_n[i] = int(ans_n[0])
    end_P23 = time.time()
    
    
    hv_n = histogram_n.argsort()[::-1][:5]  
    hv_t = histogram_t.argsort()[::-1][:5]
    
    print(tp2-tp1)

    
    #print(hv_n)
    #print(hv_t)
    
    #print('Answer : Protocol Laplace for e =', e)
    
    #The following are f1 scores
    #pre = precision(hv_t, hv_n)
    #rec = recall(hv_t, hv_n)
    #f1 = f1Score(pre, rec)
    
    err = err_measure(hv_t, hv_n, histogram_t, 0.1, e)
    
    
    

    '''
    print('Runtime(KeyGen) = ', end_P11 - start_P11)
    print('Runtime(DO_ComputeEncX) = ', (end_P12 - start_P12)/num_DO )
    print('Runtime(AS_MergeEncX) = ', end_P21 - start_P21)
    print('Runtime(AS_Construct_RangeTree) = ', end_P22 - start_P22)
    print('Runtime(AS_GenerateMasked_Hist) = ', end_P23 - start_P23)
    '''
    
    return err
    
   # compute Runtime
   
def main():
    for i in range(11):
        e = 0.1 + i * 0.2
        err_list = np.zeros(11)
        for j in range(10):
            err = evaluate_hvhitter("adult.dataset.txt", 10, 1, 1, 2, e)
            err_list[j] = err
        
        print(np.mean(err_list))
        print(np.std(err_list))
        print("   ")
    
    
if __name__== "__main__":
    main()
        
'''
e = 2
err = evaluate_hvhitter("adult.dataset.txt", 10, 1, 1, 100, e)
print(err)

err = evaluate_hvhitter("adult.dataset.txt", 10, 1, 1, 100, e)
print(err)

err = evaluate_hvhitter("adult.dataset.txt", 10, 1, 1, 100, e)
print(err)

err = evaluate_hvhitter("adult.dataset.txt", 10, 1, 1, 100, e)
print(err)

err = evaluate_hvhitter("adult.dataset.txt", 10, 1, 1, 100, e)
print(err)
'''

#a = [1.0, 0.6, 0.8, 0.6, 1.0]
#mk = np.array(a)
#print(np.mean(mk))
#print(np.std(mk))


#The following is dispatcher

'''
for i in range(10):
    e = 0.3 + i * 0.3
    err_list = np.zeros(10)
    for j in range(5):
        err = evaluate_hvhitter("adult.dataset.txt", 10, 1, 1, 100, e)
        err_list[j] = err
        
    print(np.mean(err_list))
    print(np.std(err_list))
    print("   ")
'''

        






