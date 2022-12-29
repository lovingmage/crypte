import csv
import time
import numpy as np
import math
from AS import AnalyticsServer
from CSP import CSProvider
from DO import DOwner


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
    runs=10
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

    # Phase2 step2
    start_P22 = time.time()
    As.range_tree(attr)
    size=domain_e[attr]-domain_s[attr]+1
    k=math.ceil(math.log(size,2))
    As.construct_noisyRangeTree(e/k)
    c1,c2=As.range_q(r_start,r_end)
    ans_n=csp.Laplace([c2],e/k,1)
    ans_t=csp.decryptonly([c1],1)
    print('Answer : Protocol Laplace for e =', e)
    print(ans_n)
    print(ans_t)
    
    #end_P31 = time.time()

    



   # compute Runtime
