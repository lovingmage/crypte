import csv
import time
import numpy as np
import os

from AS import AnalyticsServer
from CSP import CSProvider
from DO import DOwner

import _pickle as cPickle


def evaluate_noisemax(inputfile, num_DO, attr, r_start,r_end,e, qnum):
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
    As.set_PK(csp.getPKey())
    for d_owner in DOwners:
        d_owner.set_PK(csp.getPKey())    

    # Phase1 step2
    start_P12 = time.time()     
    for d_owner in DOwners:
        d_owner.computeEnc_X()
    end_P12 = time.time()

    # Phase2 Step 1
    print('Phase 2 : Protocol Laplace-AS')
    start_P21 = time.time()
    for d_owner in DOwners:
        enc_Xi = d_owner.getEnc_X()
        #as merges enc_Xi
        As.add_enc_X(enc_Xi,num_DO)
    end_P21 = time.time()

    # Phase2 step2
    enc_Ctilda_List = []
    start_P22 = time.time()
    f = open("./dataset/as_noise.txt", "w")
    for i in range(0, qnum - 1, 1):
        enc_Ctilda, ASnoise = As.noisecount(attr,r_start,r_end,e)
        enc_Ctilda_List.append(enc_Ctilda)
        f.write( str(ASnoise) + "\n"  )
    end_P22 = time.time()
    
    start_P22 = time.time()
    enc_Ctilda= As.Laplace(attr,r_start,r_end,e)
    end_P22 = time.time()        


    # Phase3 step1
    print('Phase 3 : Protocol Laplace-CSP')
    start_P31=time.time()
    f = open("./dataset/as_noise_count.txt", "w")
    for i in range(0, qnum - 1, 1):
        ans = csp.decrypt(enc_Ctilda_List[i], 1)
        print('Answer : Protocol Laplace')
        #print(ans[0])
        f.write( str(ans[0]) + "\n"  )
    os.system("../emp-sh2pc-master/bin/example 1 12345 & ../emp-sh2pc-master/bin/example 2 12345")
    end_P31 = time.time()

   # compute Runtime
    Runtime_KeyGen= (end_P11 - start_P11)
    Runtime_DO_ComputeEncX= ((end_P12 - start_P12)/(num_DO))
    Runtime_AS_MergeEncX= (end_P21 - start_P21)  
    Runtime_AS_Laplace= (end_P22 - start_P22)
    Runtime_CSP_Laplace= (end_P31 - start_P31)
   


    print('Runtime(KeyGen) = ', Runtime_KeyGen)
    print('Runtime(DO_ComputeEncX) = ', Runtime_DO_ComputeEncX)
    print('Runtime(AS_MergeEncX) = ', Runtime_AS_MergeEncX)
    print('Runtime(AS_Laplace) = ', Runtime_AS_Laplace)
    print('Runtime(CSP_Laplace) = ', Runtime_CSP_Laplace)
