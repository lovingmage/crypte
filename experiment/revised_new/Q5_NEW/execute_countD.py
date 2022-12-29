import numpy as np
import argparse
from countD import evaluate_countD




# read parameter values from a command line 
parser = argparse.ArgumentParser(description='Todo', epilog='Usage Example : python3 execute.py -attr 1 -r_start 5 -r_end 25 -e 0.1')
parser.add_argument('-f','--file', type=str, help='Input data file')
parser.add_argument('-attr', '--attribute', type=int, help='the attribute of interest')
parser.add_argument('-Q', '--query', type=str, help='the start of the range for attribute attr')
parser.add_argument('-e', '--epsilon',type=float, help='the privacy parameter')
parser.add_argument('-nd', '--num_DO',type=int, help='the total number of data owners')
args = parser.parse_args()


if __name__ == '__main__':

    

    
    # evaluate the protocol
    n=evaluate_countD(args.file,args.num_DO,args.attribute,args.query,args.epsilon)
    

    # The following is dispatcher
    
    print(n)
    
    #The following is dispatcher
    
        
    
