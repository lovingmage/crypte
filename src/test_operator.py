#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 30 19:26:47 2021

@author: lovingmage
"""


import unittest
import resource
import phe.paillier as paillier
import crypte.provision as pro
import crypte.core as cte
from crypte.core import Cdata


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
        #encfilter = x.filter(2,3,4)
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
            
        enc_project = cte.project(x,3)
        encnt = enc_project.count()
        m = pro.lab_decrypt(prikey, encnt)
        
        g_truth = 3*(arr0[-1] + arr0[-2])
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
        
    def test_cosprod(self):
        x = Cdata(attr=[2,5,2])
        r_init = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        pubkey, prikey = paillier.generate_paillier_keypair()
        x.set_pk(pubkey)
        arr0 = [1,2,3,7,5,6,7,8,9]
        c = pro.lab_encrypt_vector(pubkey, arr0)
            
        x.insert(c) 
        x.insert(c) 
        x.insert(c) 
            
        cosproduct = cte.cosprod(x, 1, 2, pubkey)
        m = pro.lab_mult_dec_vector(prikey, cosproduct.get_data()[0])
        g_truth = [3, 7, 5, 6, 7, 6, 14, 10, 12, 14]
        self.assertEqual(g_truth, m)

        
        
if __name__ == '__main__':
    unittest.main()
