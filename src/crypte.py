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
import util
import json
import provision as pro

        

def group_count(v):
    _v = v[0]
    for i in range(1, len(v), 1):
        _v = pro.lab_add_vector(_v, v[i])
    return _v

def enc_count(v):
    _v = []
    for elem in v:
        _v = _v + elem
    return pro.lab_sum_vector(_v)
     

'''
     Operator filter: filter the data that satisfies certain predicate
     @param attr_pred - i-th attribute
     @param val_pred_1 - value range start
     @param val_pred_2 - value range end.
     Example 
           Point query: filter(2,3,3), SELECT * From Tb WHERE 2nd_attr = value-3
           Range query: filter(2,1,3), SELECT * FROM Tb WHERE 2nd_attr in (value-1, value-3)
    '''
def filter(obj, attr_pred, val_pred_1, val_pred_2):
    
    filtered_tab = []
    attr = obj.get_attr()
    zero = obj.get_zero()
    pk = obj.get_pk()
    data = obj.get_data()
    
    
    res = Cdata(attr)
    res.set_pk(pk)
    filtered_tab = op_filter(data, attr, attr_pred, val_pred_1, val_pred_2, zero)
    res.set_data(filtered_tab)
    return res
        
    
def op_filter(tab, attr, attr_pred, val_pred_1, val_pred_2, zero):
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
        if db == None:
            self.db = []
        else:self.db = db
    
    #
    def set_pk(self, pubkey):
        self.pk = pubkey
        self.zero = pro.lab_encrypt(pubkey, 0)
        self.pk_flag = 1
        
    def fn_set_pk(self, pk_fname):
        # TODO: Implement read pk from file
        self.pk = pk_fname
        
    def set_data(self, data):
        # TODO: Implement read pk from file
        self.db = data
        
    def get_attr(self):
        return self.attr
    
    def get_pk(self):
        return self.pk
    
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
     Operator filter: filter the data that satisfies certain predicate
     @param attr_pred - i-th attribute
     @param val_pred_1 - value range start
     @param val_pred_2 - value range end.
     Example 
           Point query: filter(2,3,3), SELECT * From Tb WHERE 2nd_attr = value-3
           Range query: filter(2,1,3), SELECT * FROM Tb WHERE 2nd_attr in (value-1, value-3)
    '''
    def filter(self, attr_pred, val_pred_1, val_pred_2):
        filtered_tab = []
        if self.pk_flag == 0:
            raise ValueError('The pk has not been assigned, please setup the pk then try again.')
        if attr_pred > self.nattr:
            raise ValueError('Non existing attrbute.')
        else:
            if val_pred_1 > self.attr[attr_pred - 1] or val_pred_2 > self.attr[attr_pred - 1]:
                raise ValueError('Attribute value out of index.')
            if val_pred_1 > val_pred_2:
                raise ValueError('Wrong value order.')
            if val_pred_1 <= 0 or val_pred_1 <= 0:
                raise ValueError('Wrong attribute value.')
        
        idxbase = sum(self.attr[:attr_pred-1])
        idx1 = idxbase + val_pred_1 - 1
        idx2 = idxbase + val_pred_2
        # if point query
        if (val_pred_1 == val_pred_2):
            for elem in self.db:
                filtered_tab.append([elem[i] if i == idx1 else self.zero for i in range(len(elem))]) 
            self.db = filtered_tab
            return self
        # if range query
        else:
            for elem in self.db:
                filtered_tab.append([elem[i] if i >= idx1 and i < idx2 else self.zero for i in range(len(elem))]) 
            self.db = filtered_tab
            return self
     
    '''
     Operator project: project the data according to certain predicate, discard all other columns
     @param attr_pred - i-th attribute
     Example 
           Project query: project(2), only remain the 2nd attribute, discard other columns
    '''
    def project(self, attr_pred):
        if attr_pred > self.nattr:
            raise ValueError('Non existing attrbute.')
        idxbase = sum(self.attr[:attr_pred-1])
        idx = self.attr[attr_pred-1]
        self.db = [elem[idxbase:idxbase+idx] for elem in self.db]
        del self.attr[attr_pred-1]
        return self
    
    
    '''
     Operator group by: group by and count the data via given predicate
     @param attr_pred - i-th attribute
     Example 
           Group by query: group_by(2), SELECT COUNT(*) From Tb Group By 2nd-attribute
    '''
    def group_by(self, attr_pred):
        self.project(attr_pred)
        return group_count(self.db)
    
    #def cross_product(self, attr_left, attr_right):
        
        
    '''
     Operator count: aggregate the ones in the given table
    '''
    def count(self):
        return enc_count(self.db)
            


    
