import numpy as np
import argparse
from cp import evaluate_cp2_2




# read parameter values from a command line 
parser = argparse.ArgumentParser(description='Todo', epilog='Usage Example : python3 execute.py -attr 1 -r_start 5 -r_end 25 -e 0.1')
parser.add_argument('-f','--file', type=str, help='Input data file')
parser.add_argument('-attr1', '--attribute1', type=int, help='the attribute of interest')
parser.add_argument('-attr2', '--attribute2', type=int, help='the attribute of interest')
parser.add_argument('-Q', '--query', type=str, help='the start of the range for attribute attr')
parser.add_argument('-e', '--epsilon',type=float, help='the privacy parameter')
parser.add_argument('-nd', '--num_DO',type=int, help='the total number of data owners')
args = parser.parse_args()


if __name__ == '__main__':

    

    
    # evaluate the protocol
    #n=evaluate_cp2(args.file,args.num_DO,args.attribute1,args.attribute2,args.query,args.epsilon)
    n=evaluate_cp2_2(args.file,args.num_DO,args.attribute1,args.attribute2,args.query,args.epsilon)
    #print (n)
    
    # The following is dispatcher
    '''
    reps = 5
    for i in range(10):
        e = 0.05 + 0.2 * i
        err_list = np.zeros(reps)
        
        for j in range(reps):
            n=evaluate_cp2(args.file,args.num_DO,args.attribute1,args.attribute2,args.query, e)
            err_list[j] = 2*n
            
        print(np.mean(err_list))
        print(np.std(err_list))
        print(" ")
    '''


