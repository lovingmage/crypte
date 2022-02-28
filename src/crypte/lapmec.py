import numpy as np
import random
from sklearn.isotonic import IsotonicRegression  
import math
import time



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


