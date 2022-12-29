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

def err_measure(ref, predicted, histogram_t, delta, e):
    sum_cnt = 0
    slack = (1/e) * math.log(1/delta)
    #print (slack)
    #print (histogram_t)
    for j in predicted:
        if (j not in ref) and (histogram_t[j] < (histogram_t[ref[-1]] - slack )):
            sum_cnt += 1
            
    return (len(ref) - sum_cnt)/len(ref)

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
        X[i] = D[i][1]
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


def error_metric():
    #abs_error = 0.0
    #tcount = 0
    #ncount = 0
    
    
    t_rank = np.argsort(REAL_DIST)
    t_rank= t_rank[::-1][:5]
    n_rank = np.argsort(ESTIMATE_DIST)
    n_rank= n_rank[::-1][:5]
    
    
    '''
    for i in range(4, 25, 1):
        tcount += REAL_DIST[i]
        ncount += ESTIMATE_DIST[i]
    '''
    '''
    for x in range(domain):
        # print REAL_DIST[x], ESTIMATE_DIST[x]
        abs_error += np.abs(REAL_DIST[x] - ESTIMATE_DIST[x]) ** 2
    return abs_error / domain
    '''
    #The following is f1 score
    #pre = precision(t_rank, n_rank)
    #rec = recall(t_rank, n_rank)
    
    err = err_measure(t_rank, n_rank, REAL_DIST, 0.1, args.epsilon)
    
    return err
    


def main():
    generate_auxiliary()
    generate_dist_fromfile("uci_adult_sorted.txt")
    results = np.zeros(args.exp_round)
    for i in range(args.exp_round):
        perturb()
        aggregate()
        results[i] = error_metric()
    #print (results)
    print (np.mean(results), np.std(results))


def dispatcher():
    global g
    for e in np.arange(0.1, 3.1, 0.3):
        start_P1 = time.time()

        print("    ")
        #print (e) 
        args.epsilon = float(e)
        # try other g
        g = args.projection_range
        # OLH
        g = int(round(math.exp(args.epsilon))) + 1
        #print (g) 
        main()
        
        end_P1 = time.time()
        #print(REAL_DIST)
        #print("The Running Time for this round is : ")
        #print (end_P1 - start_P1)


parser = argparse.ArgumentParser(description='Comparisor of different schemes.')
parser.add_argument('--domain', type=int, default=101,
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