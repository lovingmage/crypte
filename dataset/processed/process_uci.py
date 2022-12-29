#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 15:56:50 2019

@author: lovingmage
"""


def readfile(fn):
    D = []
    f = open(fn)
    for i in f.readlines():
        if len(i.split(',')) > 2:
            D.append(i)
    return D



lookup = {
        "United-States" : 1, 
        "Cambodia" : 2, 
        "England" : 3, 
        "Puerto-Rico" : 4, 
        "Canada" : 5, 
        "Germany" : 6, 
        "Outlying-US(Guam-USVI-etc)" : 7, 
        "India" : 8, 
        "Japan" : 9, 
        "Greece" : 10, 
        "South" : 11, 
        "China" : 12, 
        "Cuba": 13, 
        "Iran" : 14, 
        "Honduras" : 15, 
        "Philippines" : 16, 
        "Italy" :17, 
        "Poland" : 18, 
        "Jamaica" : 19, 
        "Vietnam" : 20, 
        "Mexico" : 21, 
        "Portugal" : 22, 
        "Ireland" : 23, 
        "France" : 24, 
        "Dominican-Republic" :25, 
        "Laos" : 26, 
        "Ecuador" : 27, 
        "Taiwan" : 28,
        "Haiti" : 29, 
        "Columbia" : 30, 
        "Hungary" : 31, 
        "Guatemala" :32, 
        "Nicaragua" : 33, 
        "Scotland" : 34, 
        "Thailand" : 35, 
        "Yugoslavia" : 36, 
        "El-Salvador" : 37, 
        "Trinadad&Tobago" : 38, 
        "Peru" : 39, 
        "Hong" : 40, 
        "Holand-Netherlands" : 41,
        "?" : 42}

lookup_gender = {"Male":1, "Female":2}


def process_data(D, fn):
    processed_D = []
    f = open(fn, "w")
    for i in D:
        record = i.split(',')
        national = lookup[record[13].strip()]
        gender = lookup_gender[record[9].strip()]
        out = str(gender) + ',' + str(record[0].strip()) + ',' + str(record[4].strip()) + ',' + str(national) + '\n'
        f.write(out)
        
D = readfile("./uci.adult.100.sorted.txt")
tmp = 0
for i in D:
    record = i.split(',')
    if (record[0] == '1') and (record[1] == '30') and (record[3] == '21\n'):
        tmp+=1
print (tmp)
    
#process_data(D, "uci_adult_1000.txt")
    