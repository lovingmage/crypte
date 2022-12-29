#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 18 18:43:25 2021

@author: lovingmage
"""


import random
import unittest
import phe.paillier as paillier
import resource
import crypte.provision as pro
import json
import os
from crypte import util

class TestClient(unittest.TestCase):
    
    # Test lab operations
    def test_lab_op(self):
        r_init = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        pubkey, prikey = paillier.generate_paillier_keypair()
        arr0 = []
        arr1 = []
        # Addition
        for i in range(10):
            m1 = random.randrange(500)
            m2 = random.randrange(500)
            c = pro.lab_encrypt(pubkey, m1)
            c2 = pro.lab_encrypt(pubkey, m2)
            c3 = pro.lab_add(c, c2)
            m = pro.lab_decrypt(prikey, c3)
            arr0.append(m)
            arr1.append(m1+m2)
            
        # Subtraction
        for i in range(10):
            m1 = random.randrange(500)
            m2 = random.randrange(500)
            c = pro.lab_encrypt(pubkey, m1)
            c2 = pro.lab_encrypt(pubkey, m2)
            c3 = pro.lab_sub(c, c2)
            m = pro.lab_decrypt(prikey, c3)
            arr0.append(m)
            arr1.append(m1-m2)
        self.assertEqual(arr0, arr1)
        
    # Test labhe add vec
    def test_lab_add_vec(self):
        r_init = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        pubkey, prikey = paillier.generate_paillier_keypair()
        arr0 = [random.randrange(500) for i in range(100)]
        arr1 = [random.randrange(500) for i in range(100)]
        sum_m = [arr0[i] + arr1[i] for i in range(100)]
        c0 = pro.lab_encrypt_vector(pubkey, arr0)
        c1 = pro.lab_encrypt_vector(pubkey, arr1)
        c = pro.lab_add_vector(c0, c1)
        m = pro.lab_decrypt_vector(prikey, c)
        self.assertEqual(sum_m, m)
        
    # Test labhe sub vec
    def test_lab_sub_vec(self):
        r_init = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        pubkey, prikey = paillier.generate_paillier_keypair()
        arr0 = [random.randrange(500) for i in range(100)]
        arr1 = [random.randrange(500) for i in range(100)]
        sum_m = [arr0[i] - arr1[i] for i in range(100)]
        c0 = pro.lab_encrypt_vector(pubkey, arr0)
        c1 = pro.lab_encrypt_vector(pubkey, arr1)
        c = pro.lab_sub_vector(c0, c1)
        m = pro.lab_decrypt_vector(prikey, c)
        self.assertEqual(sum_m, m)
        
    # Test labhe multiplication
    def test_lab_mult(self):
        r_init = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        pubkey, prikey = paillier.generate_paillier_keypair()
        arr0 = []
        arr1 = []
        for i in range(10):
            m1 = random.randrange(500)
            m2 = random.randrange(500)
            c = pro.lab_encrypt(pubkey, m1)
            c2 = pro.lab_encrypt(pubkey, m2)
            c3 = pro.lab_mult(pubkey, c, c2)
            m = pro.lab_mult_dec(prikey, c3)
            arr0.append(m)
            arr1.append(m1*m2)
        self.assertEqual(arr0, arr1)
        
    # Test batch operation
    def test_lab_batch(self):
        r_init = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        pubkey, prikey = paillier.generate_paillier_keypair()
        arr0 = [random.randrange(500) for i in range(100)]
        c = pro.lab_encrypt_vector(pubkey, arr0)
        m = pro.lab_decrypt_vector(prikey, c)
        self.assertEqual(arr0, m)
        
    def test_lab_sum_vector(self):
        r_init = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        pubkey, prikey = paillier.generate_paillier_keypair()
        arr0 = [random.randrange(500) for i in range(100)]
        summation = sum(arr0)
        c = pro.lab_encrypt_vector(pubkey, arr0)
        sumc = pro.lab_sum_vector(c)
        m = pro.lab_decrypt(prikey, sumc)
        self.assertEqual(summation, m)
        
    def test_mult_re(self):
        r_init = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        pubkey, prikey = paillier.generate_paillier_keypair()
        a = 10
        b = 15
        seed = 7
        num1 = pro.lab_encrypt(pubkey, a)
        num2 = pro.lab_encrypt(pubkey, b)
        c = pro.lab_mult(pubkey, num1, num2)
        m = pro.lab_mult_dec(prikey, c)
        
        c_re = pro.lab_mult_re(pubkey, c, seed)
        m_re = pro.lab_mult_dec(prikey, c_re)
        self.assertEqual(m, m_re - seed)

        
    def test_serialize(self):
        r_init = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        pubkey, prikey = paillier.generate_paillier_keypair()
        data = util.generate_random_data(2,2)
        
        env = pro.encrypt_vector(pubkey, data)
        #print("size is", sys.getsizeof(env))
        
        enc_with_one_pub_key = {}
        enc_with_one_pub_key['public_key'] = {'g': pubkey.g,'n': pubkey.n}
        enc_with_one_pub_key['values'] = [ (str(x.ciphertext()), x.exponent) for x in env ]
        serialised = json.dumps(enc_with_one_pub_key)
        # Writing to sample.json
        with open("sample.json", "w") as outfile:
            outfile.write(serialised)
        
            # Opening JSON file
        with open('sample.json', 'r') as openfile:
          
            # Reading from json file
            data_in = json.load(openfile)
        
        _in_serialised =json.dumps(data_in)
        received_dict = json.loads(_in_serialised)
        
        
        pk = received_dict['public_key']
        pubkey = paillier.PaillierPublicKey(n=int(pk['n']))
        enc_nums_rec = [paillier.EncryptedNumber(pubkey, int(x[0]), int(x[1])) for x in received_dict['values']]
        
        
        mvec = pro.decrypt_vector(prikey, enc_nums_rec)
        os.system('rm sample.json')
        self.assertEqual(list(mvec), data)
        
            
    def test_serialize_lab(self):
        r_init = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        pubkey, prikey = paillier.generate_paillier_keypair()
        data = util.generate_random_data(2,2)
        
        lab_env = pro.lab_encrypt_vector(pubkey, data)
        env = [elem[1] for elem in lab_env]
        lab = [elem[0] for elem in lab_env]
        
        #print("size is", sys.getsizeof(env))
        
        enc_with_one_pub_key = {}
        enc_with_one_pub_key['public_key'] = {'g': pubkey.g,'n': pubkey.n}
        enc_with_one_pub_key['values'] = [ (str(x.ciphertext()), x.exponent) for x in env ]
        serialised = json.dumps(enc_with_one_pub_key)
        # Writing to sample.json
        with open("sample.json", "w") as outfile:
            outfile.write(serialised)
        
            # Opening JSON file
        with open('sample.json', 'r') as openfile:
          
            # Reading from json file
            data_in = json.load(openfile)
        
        _in_serialised =json.dumps(data_in)
        received_dict = json.loads(_in_serialised)
        
        
        pk = received_dict['public_key']
        pubkey = paillier.PaillierPublicKey(n=int(pk['n']))
        enc_nums_rec = [paillier.EncryptedNumber(pubkey, int(x[0]), int(x[1])) for x in received_dict['values']]
        
        rec_lab_env = [ [lab[i], enc_nums_rec[i] ] for i in range(len(lab)) ]
        mvec = pro.lab_decrypt_vector(prikey, rec_lab_env)
        os.system('rm sample.json')
        self.assertEqual(list(mvec), data)
        
        
if __name__ == '__main__':
    unittest.main()
