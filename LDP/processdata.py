#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 13 14:25:30 2019

@author: lovingmage
"""
import numpy as np
import argparse
import csv

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
    return D
    
def write_to_external(my_list):
    with open('dataset.txt', 'w') as f:
        for item in my_list:
            out = item[0] + ',' + item[1] + ',' + item[2] + ',' + item[3] + ',' + item[4]
            f.write("%s\n" % out)
            
def prod_gender_age(my_data):
    for i in range(len(my_data)):
        if my_data[i][0] == '1':
            tmp = str(int(my_data[i][1]))
            my_data[i].append(tmp)
        if my_data[i][0] == '2':
            tmp = str(2*int(my_data[i][1]))
            my_data[i].append(tmp)
            
    #print (my_data[19])
    return my_data
   
    
    
parser = argparse.ArgumentParser(description='Comparisor of different schemes.')
parser.add_argument('--domain', type=int, default=100,
                    help='specify the domain of the representation of domain')
parser.add_argument('--n_user', type=int, default=33000,
                    help='specify the number of data point, default 10000')
parser.add_argument('--exp_round', type=int, default=50,
                    help='specify the n_userations for the experiments, default 10')
parser.add_argument('--epsilon', type=float, default=2,
                    help='specify the differential privacy parameter, epsilon')
parser.add_argument('--projection_range', type=int, default=2,
                    help='specify the domain for projection')
args = parser.parse_args()

data = generate_dist_fromfile("testfile.txt")
prod_age_gen = prod_gender_age(data)
write_to_external(prod_age_gen)