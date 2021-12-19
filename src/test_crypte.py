#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 30 19:26:47 2021

@author: lovingmage
"""


import unittest
import numpy as np
import random
import resource
import time
import phe.paillier as paillier
from dataclasses import dataclass
import util
import json
import provision as pro
from crypte import Cdata
import crypte as cte

class TestClient(unittest.TestCase):
    def test_filter(self):
        x = Cdata(attr=[2,5,2])
        r_init = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        pubkey, prikey = paillier.generate_paillier_keypair()
        x.set_pk(pubkey)
        arr0 = [1,2,3,7,5,6,7,8,9]
        c = pro.lab_encrypt_vector(pubkey, arr0)
            
        x.insert(c) 
        x.insert(c) 
        x.insert(c) 
            
        encfilter = cte.filter(x, 2,3,4)
        encnt = encfilter.count()
        m = pro.lab_decrypt(prikey, encnt)
        
        g_truth = 3 * (arr0[4] + arr0[5])
        self.assertEqual(g_truth, m)
           
        
    def test_project(self):
        x = Cdata(attr=[2,5,2])
        r_init = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        pubkey, prikey = paillier.generate_paillier_keypair()
        x.set_pk(pubkey)
        arr0 = [1,2,3,7,5,6,7,8,9]
        c = pro.lab_encrypt_vector(pubkey, arr0)
            
        x.insert(c) 
        x.insert(c) 
        x.insert(c) 
            
        enc_project = x.project(1)
        encnt = enc_project.count()
        m = pro.lab_decrypt(prikey, encnt)
        
        g_truth = 3*(arr0[0] + arr0[1])
        self.assertEqual(g_truth, m)
        
    def test_groupby(self):
        x = Cdata(attr=[2,5,2])
        r_init = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        pubkey, prikey = paillier.generate_paillier_keypair()
        x.set_pk(pubkey)
        arr0 = [1,2,3,7,5,6,7,8,9]
        c = pro.lab_encrypt_vector(pubkey, arr0)
            
        x.insert(c) 
        x.insert(c) 
        x.insert(c) 
            
        enc_gby = x.group_by(2)
        m = pro.lab_decrypt_vector(prikey, enc_gby)
        g_truth = [3*elem for elem in arr0[2:7]]
        self.assertEqual(g_truth, m)
        
        
if __name__ == '__main__':
    unittest.main()
