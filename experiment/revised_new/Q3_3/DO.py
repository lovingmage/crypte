import numpy as np
from operator import mul
from labScheme import localGen
from util import space_mapping

#Data Owner
class DOwner:
    def __init__(self, D, domain_s, domain_e):
        self.D = D
        self.domain_s = domain_s
        self.domain_e = domain_e
        self.mpk = None
        self.labEnc_X = None        # compute Enc(X) locally
        self.l=4
        self.seed=self.enc_seed=None

    def set_MPK(self, mpk):
        self.mpk = mpk
        self.seed,self.enc_seed=localGen(mpk)



    def computeXsize(self):
        """
        Protocol-Compute the size of X
	:return sz
        """
        sz=0
        for i in range(self.l):
            sz=sz+self.domian_e[i]-self.domain_s[i]+1
        return sz




    def computeEnc_X(self):
        """
        Protocol-Encrypt One-Hot-Coding(local computation)
        :return enc_X: encrypted D in 1-hot-coding
        """
        # Encrypt one-hot-coding
        self.enc_X=[[] for i in range(self.l)]
        ind=[]
        for i in range(self.l):
            ind.append(int(self.D[i])-self.domain_s[i])
        k=0
        for i in range(self.l):
            for j in range(self.domain_e[i]-self.domain_s[i]+1):
                if(j!=ind[i]):
                    self.enc_X[i].append(self.mpk.labEncrypt(self.seed,1,0,self.enc_seed))
                else:
                    self.enc_X[i].append(self.mpk.labEncrypt(self.seed,1,1,self.enc_seed))
                k=k+1
    # To send enc_X to AS 
    def getEnc_X(self):
        return self.enc_X
    
    def getEnc_Seed(self):
        return self.enc_seed
