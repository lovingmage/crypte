import argparse
import math
import numpy as np
import xxhash
import csv
import time
from sklearn.metrics import f1_score



domain = 0
epsilon = 0.0
n = 0
g = 0

X = []
Y = []

REAL_DIST = []
ESTIMATE_DIST = []

p = 0.0
q = 0.0


def generate():
    # uniform distribution. one can also use other distributions
    #x = np.random.randint(domain)
    x = np.random.zipf(domain)
    return x

'''
@prarm : inputfile
This function will read the UCI file and parse the corresponding attribute
'''
def generate_dist_fromfile(inputfile):
    global X, REAL_DIST
    X = np.zeros(args.n_user, dtype=np.int)
    
    # Read Data from Outside
    D=[[] for i in range(args.n_user)]
    with open(str(inputfile)) as csv_file:
     csv_reader = csv.reader(csv_file, delimiter=',')
     line_count = 0
     i=0    
     for row in csv_reader:
        if(line_count<args.n_user):
           D[line_count]=row
           line_count=line_count+1
        else:
           break
       
    for i in range(args.n_user):
        # Read the 1st Attribute
        #print (D[i][1])
        X[i] = D[i][0]
        REAL_DIST[X[i]] += 1
    
    #print(REAL_DIST)
       

def generate_dist():
    global X, REAL_DIST
    X = np.zeros(args.n_user, dtype=np.int)
    for i in range(args.n_user):
        X[i] = generate()
        REAL_DIST[X[i]] += 1


def generate_auxiliary():
    global ESTIMATE_DIST, REAL_DIST, n, p, q, epsilon, domain
    domain = args.domain
    epsilon = args.epsilon

    n = args.n_user

    REAL_DIST = np.zeros(domain)
    ESTIMATE_DIST = np.zeros(domain)

    p = math.exp(epsilon) / (math.exp(epsilon) + args.projection_range - 1)
    q = 1.0 / (math.exp(epsilon) + args.projection_range - 1)


def perturb():
    global Y
    Y = np.zeros(n)
    for i in range(n):
        v = X[i]
        x = (xxhash.xxh32(str(v), seed=i).intdigest() % g)
        y = x

        p_sample = np.random.random_sample()
        if p_sample > p:
            # perturb
            y = np.random.randint(0, g - 1)
            if y >= x:
                y += 1
        Y[i] = y


def aggregate():
    global ESTIMATE_DIST
    ESTIMATE_DIST = np.zeros(domain)
    for i in range(n):
        for v in range(domain):
            if Y[i] == (xxhash.xxh32(str(v), seed=i).intdigest() % g):
                ESTIMATE_DIST[v] += 1
    a = 1.0 * g / (p * g - 1)
    b = 1.0 * n / (p * g - 1)
    ESTIMATE_DIST = a * ESTIMATE_DIST - b

# The following is metric for count error

def error_metric():
    abs_error = 0.0
    
    #The following is for marginal
    for x in range(domain):
        # print REAL_DIST[x], ESTIMATE_DIST[x]
        abs_error += np.abs(REAL_DIST[x] - ESTIMATE_DIST[x]) 
    
    
    #abs_error = np.abs(REAL_DIST[1] - ESTIMATE_DIST[1]) 
    #print(ESTIMATE_DIST)
    #print(ESTIMATE_DIST[599])
    #print(REAL_DIST[599])
    
    return abs_error 

    
# This error metric is for q6,q7
'''
def error_metric(): 
    #print (ESTIMATE_DIST)
    tcnt = 0
    ncnt = 0
    for i in REAL_DIST:
        if int(i) <= 0:
            continue
        else:
            tcnt = tcnt + 1  
            
    for j in ESTIMATE_DIST:
        if int(j) <= 0:
            continue
        else:
            ncnt = ncnt + 1  
    return abs(tcnt - ncnt)
'''
    
def convert_to_log_err(err):
    log10err = np.zeros(len(err))
    for i in range(len(err)):
        log10err[i] = math.log10(err[i] + 1)
    return log10err

def main():
    generate_auxiliary()
    generate_dist_fromfile("testfile.txt")
    results = np.zeros(args.exp_round)
    for i in range(args.exp_round):
        perturb()
        aggregate()
        results[i] = error_metric()
    #print (results)
    log_results = convert_to_log_err(results)
    #print (results)
    print (np.mean(results),np.std(results),log_results.mean(),log_results.std() )


def dispatcher():
    global g
    for e in np.arange(0.1, 2.0, 0.2):
        start_P1 = time.time()

        #print("    ")
        #print (e) 
        args.epsilon = float(e)
        # try other g
        g = args.projection_range
        # OLH
        g = int(round(math.exp(args.epsilon))) + 1
        #print (g) 
        main()
        
        end_P1 = time.time()
        #print("The Running Time for this round is : ")
        #print (end_P1 - start_P1)
        
        #print (REAL_DIST)
        #print (ESTIMATE_DIST)
        



parser = argparse.ArgumentParser(description='Comparisor of different schemes.')
parser.add_argument('--domain', type=int, default=200,
                    help='specify the domain of the representation of domain')
parser.add_argument('--n_user', type=int, default=32561,
                    help='specify the number of data point, default 10000')
parser.add_argument('--exp_round', type=int, default=10,
                    help='specify the n_userations for the experiments, default 10')
parser.add_argument('--epsilon', type=float, default=2,
                    help='specify the differential privacy parameter, epsilon')
parser.add_argument('--projection_range', type=int, default=2,
                    help='specify the domain for projection')
args = parser.parse_args()
dispatcher()