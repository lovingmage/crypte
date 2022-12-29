#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 14:44:58 2021

@author: lovingmage
"""
import numpy as np
import random
import resource
import time
import phe.paillier as paillier
from dataclasses import dataclass
import json
from provision import *
from lapmec import *
#import provision as pro
from copy import copy



'''
    Filter function that returns a new Cdata object
'''
def filter(obj, attr_pred, val_pred_1, val_pred_2):
    if obj.check_re() == True:
        raise ValueError('Require re-encryption.')
    filtered_tab = []
    attr = obj.get_attr()
    zero = obj.get_zero()
    pk = obj.get_pk()
    data = obj.get_data()
    
    #if pk == None:
    #    raise ValueError('The pk has not been assigned, please setup the pk then try again.')
    
    res = Cdata(attr)
    res.set_pk(pk)
    filtered_tab = op_filter(data, attr, attr_pred, val_pred_1, val_pred_2, zero)
    res.set_data(filtered_tab)
    return res
        
'''
    Project function that returns a new Cdata object
'''
def project(obj, attr_pred):
    if obj.check_re() == True:
        raise ValueError('Require re-encryption.')
    attr = obj.get_attr()
    zero = obj.get_zero()
    pk = obj.get_pk()
    data = obj.get_data()
    
    #if pk == None:
    #    raise ValueError('The pk has not been assigned, please setup the pk then try again.')
    
    res = Cdata(attr)
    res.set_pk(pk)
    project_tab, nattr = op_project(data, attr, attr_pred)
    res.set_data(project_tab)
    res.set_attr(nattr)
    return res

'''
    Project function that returns a new Cdata object
'''
def cosprod(obj, attr_1, attr_2, pk):
    attr = obj.get_attr()
    zero = obj.get_zero()
    pk = obj.get_pk()
    data = obj.get_data()
    
    #if pk == None:
    #    raise ValueError('The pk has not been assigned, please setup the pk then try again.')
    
    res = Cdata(attr)
    res.set_pk(pk)
    cos_tab, nattr = op_cross(data, attr, attr_1, attr_2, pk)
    res.set_data(cos_tab)
    res.set_attr([nattr])
    res.set_re()
    return res

'''
     Operator filter: filter the data that satisfies certain predicate
     @param tab - input encrypted table
     @param attr - table schema
     @param attr_pred - i-th attribute
     @param val_pred_1 - value range start
     @param val_pred_2 - value range end.
     Example 
           Point query: filter(2,3,3), SELECT * From Tb WHERE 2nd_attr = value-3
           Range query: filter(2,1,3), SELECT * FROM Tb WHERE 2nd_attr in (value-1, value-3)
'''
def op_filter(tab, attr, attr_pred, val_pred_1, val_pred_2, zero):           
    if attr_pred > len(attr):
        raise ValueError('Non existing attrbute.')
    else:
        if val_pred_1 > attr[attr_pred - 1] or val_pred_2 > attr[attr_pred - 1]:
            raise ValueError('Attribute value out of index.')
        if val_pred_1 > val_pred_2:
            raise ValueError('Wrong value order.')
        if val_pred_1 <= 0 or val_pred_2 <= 0:
            raise ValueError('Wrong attribute value.')
            
    filtered_tab = []
    idxbase = sum(attr[:attr_pred-1])
    idx1 = idxbase + val_pred_1 - 1
    idx2 = idxbase + val_pred_2
        # if point query
    if (val_pred_1 == val_pred_2):
        for elem in tab:
            filtered_tab.append([elem[i] if i == idx1 else zero for i in range(len(elem))]) 
        return filtered_tab
    # if range query
    else:
        for elem in tab:
            filtered_tab.append([elem[i] if i >= idx1 and i < idx2 else zero for i in range(len(elem))]) 
        return filtered_tab
    
    
'''
     Operator project: project the data according to certain predicate, discard all other columns
     @param tab - input encrypted table
     @param attr - table schema
     @param attr_pred - i-th attribute
     Example 
           Project query: project(2), only remain the 2nd attribute, discard other columns
    '''
def op_project(tab, attr, attr_pred):
    project_tab = []
    if attr_pred > len(attr):
        raise ValueError('Non existing attrbute.')
    
    idxbase = sum(attr[:attr_pred-1])
    idx = attr[attr_pred-1]
    project_tab = [elem[idxbase:idxbase+idx] for elem in tab]
    del attr[attr_pred-1]
    return project_tab, attr 


'''
     Operator cross product: 
     @param tab - input encrypted table
     @param attr - table schema
     @param attr_1 - the first attribute
     @param attr_2 - the second attribute
     @param pk - public key for encryption
     Example 
           Cross product query (conjunctive query): query on attribute A and B.
'''
def op_cross(tab, attr, attr_1, attr_2, pk):
    if attr_1 > len(attr) or attr_2 > len(attr):
        raise ValueError('Attribute value out of index.')
    if attr_1 > attr_2:
        raise ValueError('Wrong value order.')
    if attr_1 <= 0 or attr_2 <= 0:
        raise ValueError('Wrong attribute value.')
        
    tab_cosprod = []
    lo_1 = sum(attr[:attr_1-1])
    hi_1 = lo_1 + attr[attr_1-1]
    
    lo_2 = sum(attr[:attr_2-1])
    hi_2 = lo_2 + attr[attr_2-1]
    for elem in tab:
        cosprod = []
        for i in range(attr[attr_1-1]):
            for j in range(attr[attr_2-1]):
                #print(lo_1+i, lo_2 + j)
                #print(lo_2 + j)
                cosprod.append( lab_mult(pk, elem[lo_1+i], elem[lo_2 + j]) )
        tab_cosprod.append(cosprod)
    return tab_cosprod, [lo_1*lo_2]
        
    


def group_count(v):
    _v = v[0]
    for i in range(1, len(v), 1):
        _v = lab_add_vector(_v, v[i])
    return _v

def enc_count(v):
    _v = []
    for elem in v:
        _v = _v + elem
    return lab_sum_vector(_v)
    

class Cdata:
    '''
    Constructor:  Set up the database schema
    @param attr:  a list of integers denote the database schema,
                  each number dentoe one attribute and the value denote
                  the domain size
                  Example schema<a,b,c> such that dom(a)=2, dom(b), dom(c)=2
                  is denoted as attr = [2,5,2]
    @param db:    an existing db setup
    '''
    def __init__(self, attr, db = None):
        self.attr = attr
        self.nattr = len(attr)
        self.dblen = sum(attr)
        self.pk = None
        self.pk_flag = 0
        self.zero = None
        self.req_re = False
        self.re = False
        if db == None:
            self.db = []
        else:self.db = db
    
    #
    def set_pk(self, pubkey):
        self.pk = pubkey
        self.zero = lab_encrypt(pubkey, 0)
        self.pk_flag = 1
        
    def fn_set_pk(self, pk_fname):
        # TODO: Implement read pk from file
        self.pk = pk_fname
        
    def set_data(self, data):
        # TODO: Implement read pk from file
        self.db = data
        
    def set_attr(self, attr):
        # TODO: Implement read pk from file
        self.attr = attr
        
    def set_re(self):
        # TODO: Implement read pk from file
        self.re = True
        
    
    def check_re(self):
        # TODO: Implement read pk from file
        return self.req_re
        
    def get_attr(self):
        return self.attr
    
    def get_pk(self):
        return self.pk
    
    def get_pk_flag(self):
        return self.pk_flag
    
    def get_zero(self):
        return self.zero
    
    def get_data(self):
        return self.db
    
        
    def insert(self, enc_vec):
        if len(enc_vec) == self.dblen:
            self.db.append(enc_vec)
        else:
            raise ValueError('Record size not match.\n')
            
    '''
        Transform operators
    '''
    def filter(self, attr_pred, val_pred_1, val_pred_2):
        filtered_tab = []
        if self.pk_flag == 0:
            raise ValueError('The pk has not been assigned, please setup the pk then try again.')
                
        filtered_tab = op_filter(self.db, self.attr, attr_pred, val_pred_1, val_pred_2, self.zero)
        self.db = filtered_tab
        return self
     
        
    def project(self, attr_pred):
        self.db, self.attr = op_project(self.db, self.attr, attr_pred)
        return self
    
    
    def cosprod(self, attr_1, attr_2):
        self.db, self.attr = op_cross(self.db, self.attr, attr_1, attr_2, self.pk)
        self.req_re = True
        return self
    
    
    '''
        Computing operators
    '''
    
    '''
     Operator group by: group by and count the data via given predicate
     @param attr_pred - i-th attribute
     Example 
           Group by query: group_by(2), SELECT COUNT(*) From Tb Group By 2nd-attribute
    '''
    def group_by(self, attr_pred):
        if self.re == True:
            raise ValueError('Require re-encryption.')
        self.project(attr_pred)
        return group_count(self.db)
            
        
    '''
     Operator count: aggregate the ones in the given table
    '''
    def count(self):
        if self.re == True:
            raise ValueError('Require re-encryption.')
        return enc_count(self.db)
            
class CSP:
    
    def __init__(self, sk= None, pk=None, eps = None):
        if sk != None:
            self.sk = sk
        if pk != None:
            self.pk = pk
        if eps != None:
            self.eps = eps
            
        
    def derive_key(self):
        r_init = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        pubkey, prikey = paillier.generate_paillier_keypair()
        self.sk = prikey
        self.pk = pubkey
        return pubkey, prikey
    
    
    def reg_eps(self, eps):
        self.eps = eps
    
    def reveal_clear(self, x):
        #if self.pk == None or self.sk == None:
        #    raise ValueError('Require key derivation.')
        m = lab_decrypt(self.sk, x)
        return m
    
    def reveal_noisy(self, x, sens, eps, k=1):
        #if self.pk == None or self.sk == None:
        #    raise ValueError('Require key derivation.')
        m = lab_decrypt(self.sk, x)
        z = gen_laplace_once((eps/sens), 1)
        m = m+z
        
        return m
    
    def reveal_noisy_vector(self, x, sens, eps, k):
        #if self.pk == None or self.sk == None:
        #    raise ValueError('Require key derivation.')
        z = gen_laplace_once((eps/sens), k)
        m = [lab_decrypt(self.sk, elem) for elem in x]
        m = np.add(np.array(m), z)
        return m
    
    def reveal_clear_vector(self, x):
        #if self.pk == None or self.sk == None:
        #    raise ValueError('Require key derivation.')
        m = [lab_decrypt(self.sk, elem) for elem in x]
        return m
    
    def reveal_clear_mult_vector(self, x):
        #if self.pk == None or self.sk == None:
        #    raise ValueError('Require key derivation.')
        m = lab_mult_dec_vector(self.sk, x)
        return m
    
    def re_encrypt_mult(self, x):
        re = []
        for elem in x:
            m = lab_mult_dec_vector(self.sk, elem)
            re.append(lab_encrypt_vector(self.pk, m))
        return re
            

class AS:
    
    def __init__(self, pk=None, eps = None):
        if pk != None:
            self.pk = pk
        if eps != None:
            self.eps = eps
        self.data = []
            
    def set_key(self, pubkey):
        self.pk = pubkey
    
    def insert_to_db(self, x):
        self.data.insert(x)
        
    def load_data(self, data):
        self.data = data
        
    def execute(self, query, *args):
        if self.data == []:
            raise ValueError('No data available.')
            
        x = copy(self.data)
        return query(x, *args)
    
    def laplace_distort(self, sens, eps, k, x):
        if (k == 1):
            z = gen_laplace_once((eps/sens), 1)
            enc_z = lab_encrypt(self.pk, z[0])
            return lab_add(x, enc_z)
        else:
            z = gen_laplace_once((eps/sens), k)
            enc_z = lab_encrypt_vector(self.pk, z)
            return lab_add_vector(x, enc_z)
        
    
