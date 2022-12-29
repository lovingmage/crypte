#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 12:43:44 2019

@author: lovingmage
"""

import lapmec as lp


D = lp.read_data_to_hist("uci_adult_sorted.txt")
print(D)
ref = lp.getTopK(D)
for i in range(10):
    e = 0.1 + i * 0.2
    p2_measure = np.zeros(20)
    for j in range(20):
        predicted = lp.getTopK(D, e, mode="cdp")
        p2_measure[j] = lp.p2_err_measure(ref, predicted, D, 0.5, e)
    print(p2_measure.mean(), p2_measure.std())
        