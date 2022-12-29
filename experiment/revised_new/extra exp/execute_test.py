import numpy as np
import argparse
from testthresh import evaluate_GroupBy
from GroupBy import multi
from GroupBy import multi2



# read parameter values from a command line 
parser = argparse.ArgumentParser(description='Todo', epilog='Usage Example : python execute_new.py -f testfile.txt -q 1,23,42*2,24,24 -e 0.1 -nd 100')
parser.add_argument('-f','--file', type=str, help='Input data file')
parser.add_argument('-q', '--query', type=str, help='the query in the following format- conjucntive query with ')
#parser.add_argument('-e', '--epsilon',type=float, help='the privacy parameter')
parser.add_argument('-nd', '--num_DO',type=int, help='the total number of data owners')
args = parser.parse_args()


if __name__ == '__main__':

    

    
    # evaluate the protocol
    n=evaluate_GroupBy(args.file,args.num_DO,args.query)


