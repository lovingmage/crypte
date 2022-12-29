import numpy as np
import argparse
from LaplaceMech import evaluate_laplace, real_count
from noisemax import evaluate_noisemax


# read parameter values from a command line 
parser = argparse.ArgumentParser(description='Todo', epilog='Usage Example : python3 execute.py -attr 1 -r_start 5 -r_end 25 -e 0.1')
parser.add_argument('-f','--file', type=str, help='Input data file')
parser.add_argument('-attr', '--attribute', type=int, help='the attribute of interest')
parser.add_argument('-r_start', '--range_start', type=int, help='the start of the range for attribute attr')
parser.add_argument('-r_end', '--range_end', type=int, help='the end of the range for attribute attr')
parser.add_argument('-e', '--epsilon',type=float, help='the privacy parameter')
parser.add_argument('-nd', '--num_DO',type=int, help='the total number of data owners')
args = parser.parse_args()


if __name__ == '__main__':

    

    
    # evaluate the protocol
    #n=evaluate_laplace(args.file,args.num_DO,args.attribute,args.range_start,args.range_end,args.epsilon)
    #n = evaluate_laplace("./dataset/as_noise_100.txt", 10, 0, 18, 18, 0.5)
    n = evaluate_noisemax("./dataset/testfile.txt",10, 1, 1, 3, 0.3, 10)
    ##n = noise_freq("testfile.txt",100, 1, 1, 3, 0.8)
    #k = real_count("testfile.txt", 50, 0, 1, 1)
    #print (k)

    '''
    ep = [0.1, 0.3, 0.5, 0.7, 0.9]
    for j in ep:
        print ("Epsilon round ", j)
        noise = []
        for i in range(30, 31, 1):
            tmp = tmp = []
            for k in range(10):
                n = evaluate_laplace("./dataset/testfile.txt", 50, 0, i, 100, j)
                tmp.append(n)
            noise.append(tmp)
            
        print(noise)
    '''
