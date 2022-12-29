import numpy as np
from operator import mul


#Data Owner
class DOwner:
    def __init__(self, D, domain_s, domain_e):
        self.D = D
        self.domain_s = domain_s
        self.domain_e = domain_e
        self.pk = None
        self.enc_X = None        # compute Enc(X) locally
        self.l=2

    def set_PK(self, pk):
        self.pk = pk


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
        
        for i in range(self.l):
            for j in range(self.domain_e[i]-self.domain_s[i]+1):
                if(j!=ind[i]):
                    self.enc_X[i].append(self.pk.encrypt(0))
                else:
                    self.enc_X[i].append(self.pk.encrypt(1))

    # To send enc_X to AS 
    def getEnc_X(self):
        return self.enc_X
