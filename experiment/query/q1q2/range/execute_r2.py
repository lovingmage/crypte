import numpy as np
import argparse
from range2 import evaluate_range
from hvhitter import evaluate_hvhitter




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
    n = evaluate_range(args.file,args.num_DO,args.attribute,args.range_start,args.range_end,args.epsilon)
    #err = evaluate_range("adult.dataset.txt", 32000, 1, 10, 20, 0.1)
    #print(err)
    #The following is dispatcher
    '''
    for i in range(10):
        e = (0.1 + 0.2 * i)/100
        err_list = np.zeros(100)
        for i in range(100):
            err = evaluate_range(args.file,args.num_DO,args.attribute,args.range_start,args.range_end,e)
            err_list[i] = err
        print(np.mean(err_list))
        print(np.sum(err_list))
        print(" ")
    '''

