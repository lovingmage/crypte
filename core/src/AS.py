import random
import numpy as np
import multiprocessing as multi
from copy import deepcopy 
from operator import mul
from itertools import chain
import math


#Analytics Server
class AnalyticsServer:
    def __init__(self):
        self.pk = None
        self.merged_enc_X = []
        self.l=2
        self.num_DO=None
        self.domain_s=[1,1,20,10]
        self.domain_e=[2,100,25,12]
        '''	
        def set_dict(self):
        self.range[0]=0
        for i in range(1,self.l):
                self.range[i]=self.range[i-1]+self.domain_e[i-1]-self.domain_s[i-1]+1
        ''' 	
    def set_PK(self, pk):
        self.pk = pk


    def add_enc_X(self, enc_Xi,num_DO):
        """
        Protocol (dataset_merge)
        results merge into self.merged_enc_X
        :para enc_Xi: encrypted data recieved from DOwner_i
	    :para num_DO: number of data owners
        """
        self.num_DO=num_DO	
        for i in range(self.l):
            self.merged_enc_X.append(enc_Xi[i])

    
    def compute_index(self,attribute,value):
        #computes the index that represents the 
        ind=self.range[attribute]+value-self.domain_s[attribute]
        return ind
    
    def Projection(self,attribute):
        """
        Perform projection to retain only one-hot-codings for 'attribute'
        """
        enc_X_afterProjection=[]
        for i in range(self.num_DO):
                enc_X_afterProjection.append(self.merged_enc_X[i*self.l+attribute])
        return enc_X_afterProjection


    def Filter(self,attribute,r_start,r_end,enc_X_afterProjection):
        """
        Filter out irrelevant values from the one-hot-coding
       
        """
        enc_X_afterProjection_Filter=[[] for x in range(self.num_DO)]
        ind1=r_start-self.domain_s[attribute]
        ind2=r_end-self.domain_s[attribute]
        for i in range(self.num_DO):
            for j in range(ind1,ind2+1):
                enc_X_afterProjection_Filter[i].append(enc_X_afterProjection[i][j])
        return ind2-ind1+1,enc_X_afterProjection_Filter


    def count(self,size,enc_X_afterProjection_Filter):
        """
        Counts the requiste value 
        """
        c=0
        for i in range(self.num_DO):
            for j in range(size):
                c=c+enc_X_afterProjection_Filter[i][j]
        return c
        

    def Freq(self, attribute):
        enc_X_afterProjection=self.Projection(attribute)
        return enc_X_afterProjection

    def Laplace(self,attribute,r_start,r_end,e):
        enc_X_afterProjection=self.Projection(attribute)
        size,enc_X_afterProjection_Filter=self.Filter(attribute,r_start,r_end,enc_X_afterProjection)
        c=self.count(size,enc_X_afterProjection_Filter)
        #Computing noiseAS
        u=np.random.geometric(1-math.exp(-e))
        v=np.random.geometric(1-math.exp(-e))
        z=u-v
        enc_z=self.pk.encrypt(z)
        c+=enc_z
        enc_Ctilda=[]
        enc_Ctilda.append(c)


        return enc_Ctilda


    def noisecount(self,attribute,r_start,r_end,e):
        enc_X_afterProjection=self.Projection(attribute)
        size,enc_X_afterProjection_Filter=self.Filter(attribute,r_start,r_end,enc_X_afterProjection)
        c=self.count(size,enc_X_afterProjection_Filter)
        #Computing noiseAS
        u=np.random.geometric(1-math.exp(-e))
        v=np.random.geometric(1-math.exp(-e))
        z=u-v
        enc_z=self.pk.encrypt(z)
        c+=enc_z
        enc_Ctilda=[]
        enc_Ctilda.append(c)


        return enc_Ctilda, z
'''	
    def NoisyMax(self,attr,v,e):
        """
	Protocol- NoisyMax
	"""
        
        s=len(attr)
        C=[]
   
    def multiIndex(self,enc_Xi,num_DO):
	"""
	Generates multi-dimensional one-hot-coding
	from the one-hot-coidngs of the individual dimesions
	:param  attr,v : list of attributes with values v
	:return enc_multiX = Enc(mult_X)
	"""
        multiX=[]
'''	 