#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 17:52:56 2021

@author: lovingmage
"""

import numpy as np
import random
import resource
import time
import phe.paillier as paillier
from dataclasses import dataclass
import json
import sys
from multiprocessing import *



@dataclass
class Encrecord:
    _data: []
    _attribute: []
    _tag: []

def encrypt(pubkey, nums):
    for num in nums:
        pubkey.encrypt(num)


def decrypt(prikey, nums):
    for num in nums:
        prikey.decrypt(num)


def enc_add(nums1, nums2):
    for num1, num2 in zip(nums1, nums2):
        num1 + num2


def enc_mul(nums1, nums2):
    for num1, num2 in zip(nums1, nums2):
        num1 * num2


def time_method(method, *args):
    start = time.time()
    method(*args)
    return time.time() - start


def encrypt_vector(public_key, x):
    return [public_key.encrypt(i) for i in x]


def decrypt_vector(private_key, x):
    return np.array([private_key.decrypt(i) for i in x])


def sum_encrypted_vectors(x, y):
    if len(x) != len(y):
        raise ValueError('Encrypted vectors must have the same size')
    return [x[i] + y[i] for i in range(len(x))]



def lab_encrypt(pubkey, num):
    b = random.randint(1, 100)
    return [num - b, pubkey.encrypt(b)]

def lab_encrypt_vector(pubkey, x):
    return [lab_encrypt(pubkey, elem) for elem in x]

def lab_decrypt(prikey, num):
    b = prikey.decrypt(num[1])
    return num[0] + b

def lab_decrypt_vector(prikey, x):
    return [lab_decrypt(prikey, elem) for elem in x]


def lab_add(num1, num2):
    return [num1[0] + num2[0], num1[1] + num2[1]]

def lab_add_vector(x, y):
    return [ [x[i][0] + y[i][0], x[i][1] + y[i][1]] for i in range(len(x)) ]


def lab_sub(num1, num2):
    return [num1[0] - num2[0], num1[1] - num2[1]]

def lab_sub_vector(x, y):
    return [ [x[i][0] - y[i][0], x[i][1] - y[i][1]] for i in range(len(x)) ]

def lab_sum_vector(x):
    ret = x[0]
    for i in range(1, len(x)):
        ret = lab_add(ret, x[i])
    return ret


def lab_mult(pubkey, num1, num2):
    c1 = pubkey.encrypt(num1[0] * num2[0])
    c2 = num1[0] * num2[1]
    c3 = num1[1] * num2[0]
    return [c1+c2+c3, num1[1], num2[1]]

def lab_mult_re(pubkey, mul_res, seed):
    r = pubkey.encrypt(seed)
    return [mul_res[0]+r, mul_res[1], mul_res[2]]


def lab_mult_dec(prikey, num):
    b1 = prikey.decrypt(num[1])
    b2 = prikey.decrypt(num[2])
    return ( prikey.decrypt(num[0]) + b1*b2 )

def lab_mult_dec_vector(prikey, x):
    res = []
    for num in x:
        b1 = prikey.decrypt(num[1])
        b2 = prikey.decrypt(num[2])
        res.append(prikey.decrypt(num[0]) + b1*b2)
    return res
        
    #return [lab_decrypt(prikey, elem) for elem in x]
    #b1 = prikey.decrypt(num[1])
    #b2 = prikey.decrypt(num[2])
    #return ( prikey.decrypt(num[0]) + b1*b2 )