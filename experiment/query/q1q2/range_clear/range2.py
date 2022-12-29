import csv
import time
import numpy as np
import math
from AS import AnalyticsServer
from CSP import CSProvider
from DO import DOwner

import _pickle as cPickle


def evaluate_range(inputfile, num_DO, attr,r_start,r_end,e):
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
    DOwners = []
    for index in range(num_DO):
        DOwners.append(DOwner(D[index],domain_s,domain_e))


    # Phase1 step2
    start_P12 = time.time()     
    for d_owner in DOwners:
        '''ComputeEnc will only do encoding not encryption'''
        d_owner.computeEnc_X()
        #print("Compute Enc...")
    end_P12 = time.time()

    # Phase2 Step 1
    #print('Phase 2 : Protocol RangeQueries-AS')
    start_P21 = time.time()
    for d_owner in DOwners:
        enc_Xi = d_owner.getEnc_X()
        As.add_enc_X(enc_Xi,num_DO)
    end_P21 = time.time()
    

    # Phase2 step2
    start_P22 = time.time()
    As.range_tree(attr)
    size=domain_e[attr]-domain_s[attr]+1
    k=math.ceil(math.log(size,2))
    As.construct_noisyRangeTree(e/k)
    end_P22= time.time()
    
    start_P23 = time.time()
    c1,c2=As.range_q(r_start,r_end)
    end_P23 = time.time()
    
    
    start_P24 = time.time()
    ans_n=[c2]
    end_P24 = time.time()
    ans_t=csp.decryptonly([c1])
    

    '''
    print('Runtime(DO_ComputeEncX) = ', (end_P12 - start_P12)/num_DO )
    print('Runtime(AS_MergeEncX) = ', end_P21 - start_P21)
    print('Runtime(AS_Construct_Range_Tree) = ', end_P22 - start_P22)
    print('Runtime(AS_Laplace) = ', end_P23 - start_P23)
    print('Runtime(CSP_Laplace) = ', end_P24 - start_P24)
    '''
    print(ans_t)
    print(ans_n)
    
    #return abs(int(ans_t[0]) - int(ans_n[0]))

    
    #The following is dispatcher
    '''
    ep_runs = 10
    ep_error_list = []
    ep_errors = []
    ep_err_std = []
    for j in range(ep_runs):
        errorList = np.zeros(runs)
        for i in range(runs):
            e = (0.1 + j * 0.2)/100
            As.range_tree(attr)
            size=domain_e[attr]-domain_s[attr]+1
            k=math.ceil(math.log(size,2))
            As.construct_noisyRangeTree(e/k)
            c1,c2=As.range_q(r_start,r_end)
            ans_n=csp.Laplace([c2],e/k,1)
            ans_t=csp.decryptonly([c1])
            errorList[i] = abs(ans_n[0] - ans_t[0])
        ep_error_list.append(errorList)
        ep_errors.append(np.average(errorList))
        ep_err_std.append(np.std(errorList))
        
    print (ep_error_list)
    print (ep_errors)
    print (ep_err_std)
    '''
        

#The following is dispatcher for rd experiment
'''
n = evaluate_range("testfile.txt", 2, 1,10,12,0.1)
print(n)

for i in range(10):
        e = (10 + 20 * i)
        print ("The Epsilon Round is: e= ", e)
        err_list = np.zeros(10)
        for i in range(10):
            err = evaluate_range("testfile.txt", 2, 1, 10, 12, e)
            err_list[i] = err * 10
        print(np.mean(err_list))
        print(np.std(err_list))
        print(np.sum(err_list))
        print(" ")
'''


   # compute Runtime
