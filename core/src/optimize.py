import csv
import time
import numpy as np
import os

inputfile = "./dataset/rd_data100.txt"
num_DO = 10
domain = 100

binzise = 10
domhist = [0 for i in range(binzise)]
print(domhist)

binrange = domain/binzise
D=[[] for i in range(num_DO)]
    #Generate Dataset

f = open(inputfile)
for i in f.readlines():
    j = int( int(i) / binrange )
    domhist[j] = domhist[j] + 1

print (domhist)
