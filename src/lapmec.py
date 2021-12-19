import numpy as np
import random
from sklearn.isotonic import IsotonicRegression  
import math
import time

# The following are the interfaces for file I/Os
# read data to a list
def readData(inputfile):
    D = []
    f = open(inputfile)
    for i in f.readlines():
        #print(i)
        D.append(i.split(','))
    return D


# Read data to a histogram   
def read_data_to_hist(file, mode = "age"):
    f= open(file)
    if mode == "age":
        HIT = np.zeros(100)
        for elem in f.readlines():
            index = elem.split(',')[1]
            HIT[int(index)] += 1
    if mode == "na":
        HIT = np.zeros(45)
        for elem in f.readlines():
            index = elem.split(',')[3]
            HIT[int(index)] += 1
    if mode == "gen":
        HIT = np.zeros(2)
        for elem in f.readlines():
            index = elem.split(',')[0]
            HIT[int(index)-1] += 1
    return HIT


def sum_ones(num):
    bin_string = bin(num)
    cnt_ones = 0
    for i in bin_string:
        if i == '1':
            cnt_ones += 1
        else:
            continue
    return cnt_ones


def convert_to_log_err(err):
    log10err = np.zeros(len(err))
    for i in range(len(err)):
        log10err[i] = math.log10(err[i] + 1)
    return log10err

#Generate Laplace Once
def gen_laplace_once(e, k):
    u=np.random.geometric(1-pow(2.713,-e), k)
    v=np.random.geometric(1-pow(2.713,-e), k)
    z=u-v
    return z

#Direct Simulate Generate noise 2 times
def gen_laplace(e, k):
    u=np.random.geometric(1-pow(2.713,-e), k)
    v=np.random.geometric(1-pow(2.713,-e), k)
    z=u-v
    
    u2=np.random.geometric(1-pow(2.713,-e), k)
    v2=np.random.geometric(1-pow(2.713,-e), k)
    z2=u2-v2
    
    return z + z2


def gen_index_noise(e, l, k):
    u=np.random.geometric(1-pow(2.713,-(e/l)), k)
    v=np.random.geometric(1-pow(2.713,-(e/l)), k)
    noisyAns=u-v
    #noisyAns2 = np.random.laplace(0, k/e, 5)
    return noisyAns
    
# This is the function that generates noise list as AND csp
def addLplace(trueList, e):
    u=np.random.geometric(1-pow(2.713,-e), size=len(trueList))
    v=np.random.geometric(1-pow(2.713,-e), size=len(trueList))
    z=u-v
    
    u2=np.random.geometric(1-pow(2.713,-e), size=len(trueList))
    v2=np.random.geometric(1-pow(2.713,-e), size=len(trueList))
    z2=u2-v2
    
    noisyList = trueList + z + z2
    
    return noisyList

# This is the new f1 score measure
def p2_err_measure(ref, predicted, histogram_t, delta, e):
    sum_cnt = 0
    slack = (1/e) * math.log(1/delta)
    #print (slack)
    #print (histogram_t)
    for j in predicted:
        if (j not in ref) and (histogram_t[j] < (histogram_t[ref[-1]] - slack )):
            sum_cnt += 1
            
    return (len(ref) - sum_cnt)/len(ref)

# Get top K 
def getTopK(data_hist, e=0.1, mode="t"):
    #True top-k mode
    if mode == "t":
        return data_hist.argsort()[::-1][:5]
    
    #noise range tree mode
    if mode == "nr":
        nhist = np.zeros(len(data_hist))
        for i in range(len(data_hist)):
            tmp_noise = 0
            for j in range(sum_ones(i+1)):
                tmp_noise += gen_laplace(e, 1)
            nhist[i] = data_hist[i] + tmp_noise
        return nhist.argsort()[::-1][:5]
    
    #noisy node
    if mode == "n":
        nhist = np.zeros(len(data_hist))
        for i in range(len(data_hist)):
            nhist[i] = data_hist[i] + gen_laplace(e, 1)
        return nhist.argsort()[::-1][:5]
    
    #noisy cdp mode
    if mode == "cdp":
        nhist = np.zeros(len(data_hist))
        for i in range(len(data_hist)):
            nhist[i] = data_hist[i] + gen_laplace(e, 1)/2
        return nhist.argsort()[::-1][:5]

# This function simulates the distinct number of ages for specific gender
def simulation_distinct_age(D, gender, e):
    age_list = []
    for i in D:
        if int(i[0]) == gender:
            age_list.append(int(i[1]))
    distTnum = len(set(age_list))
    
    
    u=np.random.geometric(1-pow(2.713,-e))
    v=np.random.geometric(1-pow(2.713,-e))
    z=u-v
    
    u2=np.random.geometric(1-pow(2.713,-e))
    v2=np.random.geometric(1-pow(2.713,-e))
    z2=u2-v2
    
    distNnum = distTnum + z + z2
    
    if distNnum < 0:
        return 0
    else:
        return distTnum, distNnum
    
        
# The function to generate cdf
def generate_cdf(data_hist, mode = "t", e = 0.1):
    if mode == "t":
        cdf = np.zeros(len(data_hist))
        for i in range(len(data_hist)):
            cdf[i] = np.sum(data_hist[0:i])
        return cdf
    
    if mode == "nr":
        cdf = np.zeros(len(data_hist))
        for i in range(len(data_hist)):
            tmp_noise = 0
            for j in range(sum_ones(i+1) + 1):
                tmp_noise += gen_laplace(e/np.log2(100), 1)
            cdf[i] = np.sum(data_hist[0:i]) + tmp_noise
        tmp = np.arange(len(cdf))
        IRmodel = IsotonicRegression(y_min=0, increasing = True)
        return IRmodel.fit_transform(tmp, cdf)
    
    #range tree on clear
    if mode == "nrc":
        cdf = np.zeros(len(data_hist))
        for i in range(len(data_hist)):
            tmp_noise = 0
            for j in range(sum_ones(i+1)):
                tmp_noise += gen_laplace(e/np.log2(100), 1)
            cdf[i] = np.sum(data_hist[0:i]) + tmp_noise
        tmp = np.arange(len(cdf))
        IRmodel = IsotonicRegression(y_min=0, increasing = True)
        return IRmodel.fit_transform(tmp, cdf)
    
    if mode == "n":
        cdf = np.zeros(len(data_hist))
        for i in range(len(data_hist)):
            tmp_noise = 0
            cdf[i] = np.sum(data_hist[0:i]) + gen_laplace(e/len(data_hist), 1) + gen_laplace(e/len(data_hist), 1)
        tmp = np.arange(len(cdf))
        t = time.time()
        IRmodel = IsotonicRegression(y_min=0, increasing = True)
        ret = IRmodel.fit_transform(tmp, cdf)
        te = time.time()
        #print (te - t)
        return ret
    
    if mode == "ldp":
        cdf = np.zeros(len(data_hist))
        for i in range(len(data_hist)):
            cdf[i] = np.sum(data_hist[0:i])
        tmp = np.arange(len(cdf))
        IRmodel = IsotonicRegression(y_min=0, increasing = True)
        return IRmodel.fit_transform(tmp, cdf)
    
def index_noisy_cdf(His, bin_size, bin_number, e=0.1):
    ind_cdf = np.zeros(bin_number)
    for i in range(bin_number):
        #print(His[1:(i+1)*4+1])
        ind_cdf[i] = np.sum(His[1:(i+1)*bin_size+1]) + gen_laplace(e/bin_number, 1)
    tmp = np.arange(len(ind_cdf))
    IRmodel = IsotonicRegression(y_min=0, increasing = True)
    return IRmodel.fit_transform(tmp, ind_cdf)
    #return ind_cdf
    
def index_cdf(His, bin_size, bin_number):
    ind_cdf = np.zeros(bin_number)
    for i in range(bin_number):
        ind_cdf[i] = np.sum(His[1:(i+1)*bin_size+1])
    return ind_cdf

#D = read_data_to_hist("uci_adult_sorted.txt", mode="na")
#print(index_noisy_cdf(D, 4, 10, 0.1))

##################################################
# Following are the experiments dispatcher()
        
# This is the simulation of cdf
def list_get_l1(t_list, n_list):
    l1 = 0
    for i in range(len(t_list)):
        l1 += abs(n_list[i] - t_list[i])
    return l1
        
def simulation_cdf_exp():
    D = read_data_to_hist("uci_adult_sorted.txt")
    cdf = generate_cdf(D, "t")
    cdf= cdf/cdf[-1]
    err = np.zeros(10)
    print ("The true cdf is:")
    #print (cdf)

    for i in range(10):
        e = 0.1 + i * 0.2
        err = np.zeros(10)
        for j in range(10):
            #ncdf = generate_cdf(D, "nr", e)
            ncdf = generate_cdf(D, "n", e)
            #ncdf = generate_cdf(D, "ldp", e)
            ncdf = ncdf/ncdf[-1]
            #print ("The noisy cdf for round ", j)
            #print(ncdf)
            err[j] = np.sum(abs(ncdf - cdf))
        print(err.mean(), err.std())

        

#######################################################################################
#The following is for heavy hitter experiment
# By executing This dispatcher will simulate the exp for P2
def simulation_p2():
    cnlist = [ 0, 0, 0, 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 18,
                12, 17, 21, 21, 22, 38, 30, 38, 28, 41, 30, 30, 44, 37, 24, 26, 27, 26,
                74, 23, 24, 19, 17, 18, 23, 27, 15, 15, 23, 17, 16, 13, 14, 14, 16, 13, 2,  
                2,  9, 16,  6,  9, 11,  8,  5,  1,  3,  2,  1,  1,  2,  2,  0,  0, 
                4,  0,  1,  0,  3,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,]
    trueList = np.array(cnlist)
    
    for i in range(10):
        errList = np.zeros(10)
        for j in range(10):
            e = 0.1 + 0.2*i
            noisyList = addLplace(trueList, e)
            #print(noisyList - trueList)
            
            
            hv_t = trueList.argsort()[::-1][:5]
            hv_n = noisyList.argsort()[::-1][:5]
            
            errList[j] = p2_err_measure(hv_t, hv_n, trueList, 1, e)
        print(errList)
        print(np.mean(errList))
        print(np.std(errList))
        print(" ")
        

        
#The following is for q5
def simulation_p5():
    for i in range(19):
        e1 = (0.05 + i * 0.05)
        e2 = 1 - e1
        ind_err = np.zeros(10)
        ind_err = gen_index_noise(e1, 10, 10)
        ind_err_hi = gen_index_noise(e1, 10, 10)
        interval = np.array([642,642,642,642,642,642,642,642,642,642])
        interval = interval + ind_err_hi - ind_err
        for i in range(10):
            if ind_err[i] < 0:
                ind_err[i] = 0
            else:
                ind_err[i] = int(ind_err[i] * 0.075)
                
        lap_err = np.zeros(10)
        lap_err = gen_laplace(e2, 10)
        
        final_err = abs(lap_err - ind_err)
            
        #print(str(final_err.mean()) +' '+ str(final_err.std()))
        print(str(interval.mean()) +' '+ str(interval.std()))
        

#This section is for q6, distinct numbers
'''
D = readData('uci.100.sorted.txt')
for i in range(10):
    e1 = 0.1 + 0.2 * i
    e2 = e1/2
    error_list = np.zeros(10)
    for j in range(10):
        index = gen_index_noise(e2, 2, 1)
        if index[0] < 0:
            index[0] = 0
        distTnum, distNnum = simulation_distinct_age(D, 1, e1)
        error_list[j] = abs(distTnum - distNnum)
    print(error_list.mean())
    print(error_list.std())
    print(" ")
'''

    
#print (TNum, Num)
#The following is the the q4's optimizxation experiment
'''
for i in rang
e(10):
    e1 = (0.08 + i * 0.2)
    e2 = e1/2
    lap_err = np.zeros(10)
    for j in range(200):
        lap_err += abs(gen_laplace(e1, 10))
        
    print (lap_err.mean())
    print (lap_err.std())
    print (" ")
'''
  
'''
e = 0.7
trueList = np.random.randint(100, size=100)
noisyList = addLplace(trueList, e)

for i in range(10):
    errList = np.zeros(10)
    for j in range(10):
        e = 0.1 + 0.2*i
        noisyList = addLplace(trueList, e)
        print(noisyList - trueList)
        
        
        hv_t = trueList.argsort()[::-1][:5]
        hv_n = noisyList.argsort()[::-1][:5]
        
        errList[j] = p2_err_measure(hv_t, hv_n, trueList, 0.05, e)
    print(np.mean(errList))
    print(np.std(errList))
'''


