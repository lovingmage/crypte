
import numpy as np
import random
from paillier import generate_keypair
import math

import _pickle as cPickle

#Crypto Service Provider
class CSProvider:
    def __init__(self):
        self.pk = self.sk = None

    # Protocol Step1(key generation)
    def key_gen(self, n_length):
        self.pk, self.sk = generate_keypair(n_length = n_length)

    def Laplace(self, enc_Ctilda, e, size):
        """
        Protocol-(noisy laplacian computation)
        - receive Enc(Ctilda) from AS and decrypt them
        - add noise and compute C
        
        :param enc_Ctilda: Encryption of count with partial noise added
	:param e: Epsilon privacy budget for the program
	:param size: The length of C
	"""
        # decrypt Enc(C_tilda) 
        dec_Ctilda = []
        for i in range(size):
            dec_Ctilda.append(self.sk.decrypt(enc_Ctilda[i]))

        C=[]
        #compute noise
        for i in range(size):
            u=np.random.geometric(p=1-math.exp(-e))
            v=np.random.geometric(p=1-math.exp(-e))
            z=u-v
            #add noise
            C.append(dec_Ctilda[i]+z)	
        return C
     


    # To publish a public key to Data Owners and AS
    def getPKey(self):
        return self.pk

    #decrypt data
    def decrypt(self, enc_Ctilda, size):

        # decrypt Enc(C_tilda) 
        dec_Ctilda = []
        for i in range(size):
            dec_Ctilda.append(self.sk.decrypt(enc_Ctilda[i]))
	
        return dec_Ctilda
    
    #get private key and sent to the 

   
'''  
csp = CSProvider()
csp.key_gen(2048)
cPickle.dump(csp,open("./csp.pkl","wb"))

'''