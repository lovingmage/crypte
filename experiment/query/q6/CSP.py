
import numpy as np
import random
import operator
from labScheme import labGen, PRF, localGen
#from paillier import generate_keypair
from util import PRF, space_mapping
from operator import mul
#Crypto Service Provider
class CSProvider:
    def __init__(self):
        self.mpk = self.msk = None
        self.seed=self.enc_seed=None
    # Protocol Step1(key generation)
    def key_gen(self, n_length):
        self.mpk, self.msk = labGen(n_length)
        self.seed,self.enc_seed=localGen(self.mpk)

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
               dec_Ctilda.append(self.msk.labDecrypt(enc_Ctilda[i]))
        C=[]
	#compute noise
        for i in range(size):
            u=np.random.geometric(1-pow(2.713,-e))
            v=np.random.geometric(1-pow(2.713,-e))
            z=u-v
		#add noise
        C.append(dec_Ctilda[i]+z)	
        
        return C
    
    def Laplace_avg(self, enc_Ctilda, e,c, size):
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
               dec_Ctilda.append(self.msk.labDecrypt(enc_Ctilda[i]))
        C=[]
        #compute noise
        for i in range(size):
                u=np.random.geometric(1-pow(2.713,-e/c[i]))
                v=np.random.geometric(1-pow(2.713,-e/c[i]))
                z=u-v
                #add noise
                C.append(dec_Ctilda[i]/c[i]+z)
        return C
                
               
    def decryptonly(self,encC):
       dec=[]
       size=len(encC)
       for i in range(size):
            dec.append(self.msk.labDecrypt(encC[i]))
       return dec

    # To publish a public key to Data Owners and AS
    def get_MPK(self):
        return self.mpk
    def generate_labEncProductT(self,prod,pks,numDO):
        labEnc_prod=[[] for x  in range(len(prod))]

        for i in range(numDO):
            for j in range(len(prod[0])):
                a_tilda=self.msk.decrypt(prod[i][j])
                sigma1=self.msk.decrypt(pks[i*2][j])
                sigma2=self.msk.decrypt(pks[i*2+1][j])
                b1=space_mapping(PRF(sigma1,1,self.mpk.n),self.mpk.n)
                b2=space_mapping(PRF(sigma2,1,self.mpk.n),self.mpk.n)
                kk=space_mapping(b1*b2,self.mpk.n)
                a_tilda=a_tilda+kk
                label=1
                labEnc_prod[i].append(self.mpk.labEncrypt(self.seed,label,a_tilda,self.enc_seed))
        return labEnc_prod
    def generate_labEncProduct2(self,prod,pk1,pk2,numDO):
        labEnc_prod=[[] for x  in range(len(prod))]
        for i in range(numDO):
            for j in range(len(prod[0])):
                a_tilda=self.msk.decrypt(prod[i][j])
                sigma1=self.msk.decrypt(pk1[i][j])
                sigma2=self.msk.decrypt(pk2[i][j])
                b1=space_mapping(sigma1,self.mpk.n)
                b2=space_mapping(sigma2,self.mpk.n)
                hh=space_mapping(b1*b2,self.mpk.n)
                a_tilda+=hh
                label=1
                labEnc_prod[i].append(self.mpk.labEncrypt(self.seed,label,a_tilda,self.enc_seed))
        return labEnc_prod

    def generate_labEncProduct(self,prod,pks,numDO):
        labEnc_prod=[[] for x  in range(len(prod))]

        for i in range(len(prod)):
            for j in range(numDO):
                a_tilda=self.msk.decrypt(prod[i][j])
                sigma1=self.msk.decrypt(pks[i*2][j])
                sigma2=self.msk.decrypt(pks[i*2+1][j])
                b1=space_mapping(PRF(sigma1,1,self.mpk.n),self.mpk.n)
                b2=space_mapping(PRF(sigma2,1,self.mpk.n),self.mpk.n)
                kk=space_mapping(b1*b2,self.mpk.n)
                a_tilda=a_tilda+kk
                label=1
                labEnc_prod[i].append(self.mpk.labEncrypt(self.seed,label,a_tilda,self.enc_seed))
        return labEnc_prod
    def getpk(self):
       return self.mpk.encrypt(self.seed)

    '''
    def mul_decrypt(self,prod,pk1,pk2,size2):
        """
        Decryption for labMult
        """
        ans=[]
        size1=len(prod)
        for i in range(size2):
           sum=0
           for j in range(size1):
              sigma1=self.msk.decrypt(pk1[i][j])
              sigma2=self.msk.decrypt(pk2[i][j])
              b1=space_mapping(PRF(sigma1,1,self.mpk.n),self.mpk.n)
              b2=space_mapping(PRF(sigma2,1,self.mpk.n),self.mpk.n)
              kk=space_mapping(b1*b2,self.mpk.n)
              sum+=b1*b2
           
           a_tilda=self.msk.decrypt(prod[j])
           a_tilda=a_tilda+sum
           ans.append(a_tilda)
        return ans
        '''
        
    def mul_decrypt_enc2(self,prod,pk1,pk2,size2):
        """
        Decryption for labMult
        """
        ans=[]
        size1=len(prod)
        for i in range(size2):
           sum=0
           for j in range(size1):
              sigma1=self.msk.decrypt(pk1[i][j])
              sigma2=self.msk.decrypt(pk2[i][j])
              b1=space_mapping(PRF(sigma1,1,self.mpk.n),self.mpk.n)
              b2=space_mapping(PRF(sigma2,1,self.mpk.n),self.mpk.n)
              kk=space_mapping(b1*b2,self.mpk.n)
              sum+=b1*b2

           a_tilda=self.msk.decrypt(prod[j])
           a_tilda=a_tilda+sum
           a_tilda=self.mpk.labEncrypt(self.seed,1,a_tilda,self.enc_seed)
           ans.append(a_tilda)
        return ans
    def Lap_mul_decrypt2(self,prod,pk1,pk2,size2,e):
        """
        Decryption for labMult
        """
        ans=[]
        size1=len(prod)
        for i in range(size1):
           sum=0
           for j in range(size2):
              sigma1=self.msk.decrypt(pk1[j][i])
              sigma2=self.msk.decrypt(pk2[j][i])
              b1=space_mapping(PRF(sigma1,1,self.mpk.n),self.mpk.n)
              b2=space_mapping(PRF(sigma2,1,self.mpk.n),self.mpk.n)
              d=space_mapping(b1*b2,self.mpk.n)
              sum+=d

           a_tilda=self.msk.decrypt(prod[i])
           a_tilda=a_tilda+sum
           u=np.random.geometric(1-pow(2.713,-e))
           v=np.random.geometric(1-pow(2.713,-e))
           z=u-v
           a_tilda+=z
           ans.append(a_tilda)
        return ans
    
    
    def Lap_mul_decrypt_only(self,prod,pk1,pk2,size2,e):
        """
        Decryption for labMult
        """
        ans=[]
        size1=len(prod)
        for i in range(size1):
           sum=0
           for j in range(size2):
              sigma1=self.msk.decrypt(pk1[j][i])
              sigma2=self.msk.decrypt(pk2[j][i])
              b1=space_mapping(PRF(sigma1,1,self.mpk.n),self.mpk.n)
              b2=space_mapping(PRF(sigma2,1,self.mpk.n),self.mpk.n)
              d=space_mapping(b1*b2,self.mpk.n)
              sum+=d

           a_tilda=self.msk.decrypt(prod[i])
           a_tilda=a_tilda+sum
           ans.append(a_tilda)
        return ans
    
    def Lap_mul_decrypt(self,prod,pk1,pk2,size2,e):
        """
        Decryption for labMult and add noise
        """
        ans=[]
        size1=len(prod)
        for i in range(size1):
           sum=0
           for j in range(size2):
              sigma1=self.msk.decrypt(pk1[j][i])
              sigma2=self.msk.decrypt(pk2[j][i])
              b1=space_mapping(sigma1,self.mpk.n)
              b2=space_mapping(sigma2,self.mpk.n)
              d=space_mapping(b1*b2,self.mpk.n)
              sum+=d

           a_tilda=self.msk.decrypt(prod[i])
           a_tilda=a_tilda+sum
           u=np.random.geometric(1-pow(2.713,-e))
           v=np.random.geometric(1-pow(2.713,-e))
           z=u-v
           a_tilda+=z
           ans.append(a_tilda)
        return ans
    
    def mul_decrypt(self,prod,pk1,pk2,size2):
        """
        Decryption for labMult
        """
        ans=[]
        size1=len(prod)
        for i in range(size1):
           sum=0
           for j in range(size2):
              sigma1=self.msk.decrypt(pk1[j][i])
              sigma2=self.msk.decrypt(pk2[j][i])
              b1=space_mapping(sigma1,self.mpk.n)
              b2=space_mapping(sigma2,self.mpk.n)
              d=space_mapping(b1*b2,self.mpk.n)
              sum+=d

           a_tilda=self.msk.decrypt(prod[i])
           a_tilda=a_tilda+sum
           ans.append(a_tilda)
           
        return ans
    
        '''
        ans=[]
        size1=len(prod)
        for i in range(size2):
           sum=0
           for j in range(size1):
              sigma1=self.msk.decrypt(pk1[i][j])
              sigma2=self.msk.decrypt(pk2[i][j])
              b1=space_mapping(PRF(sigma1,1,self.mpk.n),self.mpk.n)
              b2=space_mapping(PRF(sigma2,1,self.mpk.n),self.mpk.n)
              kk=space_mapping(b1*b2,self.mpk.n)
              sum+=kk

           a_tilda=self.msk.decrypt(prod[j])
           a_tilda=a_tilda+sum
       
           ans.append(a_tilda)
        return ans
        '''
    
    def mul_decrypt_enc(self,prod,pk1,pk2):
        """
        Decryption for labMult
        """
        size1=len(pk1)
        size2=len(pk1[0])
        sum=0
        for i in range(size1):
           for j in range(size2):
              sigma1=self.msk.decrypt(pk1[i][j])
              sigma2=self.msk.decrypt(pk2[i][j])
              b1=space_mapping(PRF(sigma1,1,self.mpk.n),self.mpk.n)
              b2=space_mapping(PRF(sigma2,1,self.mpk.n),self.mpk.n)
              kk=space_mapping(b1*b2,self.mpk.n)
              sum+=kk

        a_tilda=self.msk.decrypt(prod)
        a_tilda=a_tilda+sum
        a_tilda=self.mpk.labEncrypt(self.seed,1,a_tilda,self.enc_seed)
        return a_tilda


    def Lap_mulDecrypt(self,num_DO,pk,C1,e):
        sum=0
        for i in range(num_DO):
            sigma1=self.msk.decrypt(pk[i])
            b1=space_mapping(PRF(sigma1,1,self.mpk.n),self.mpk.n)
            sum+=b1*b1
        n=len(C1)
        for i in range(n):
            C1[i]=self.msk.decrypt(C1[i])
            C1[i]=C1[i]+sum
            u=np.random.geometric(1-pow(2.713,-e))
            v=np.random.geometric(1-pow(2.713,-e))
            z=u-v
            C1[i]=C1[i]+z

        return C1    
    
    def generateEncCoding(self,cnt,k):
        """
        Generates encrypted 1-hot-coding for the given counts
        """ 
        n=len(cnt)
        code=[[] for x in range(n)]
        for i in range(n):
            for j in range(k):
             
               if(j+1==cnt[i]):
                  code[i].append(self.mpk.labEncrypt(self.seed,1,1,self.enc_seed))
               else:
                  code[i].append(self.mpk.labEncrypt(self.seed,1,0,self.enc_seed))

        return code

    def generateEncNoisyCoding(self,cnt,k,e):
        """
        Generates encrypted 1-hot-coding for the given counts
        """
        n=len(cnt)
        code=[[] for x in range(n)]
        for i in range(n):
            u=np.random.geometric(1-pow(2.713,-e))
            v=np.random.geometric(1-pow(2.713,-e))
            z=u-v
            cnt[i]+=z
        for i in range(n):
            for j in range(k):

               if(j+1==cnt[i]):
                  code[i].append(self.mpk.labEncrypt(self.seed,1,1,self.enc_seed))
               else:
                  code[i].append(self.mpk.labEncrypt(self.seed,1,0,self.enc_seed))

        return code
    
    def labencrypt_num(self, c_r):
        return self.mpk.labEncrypt(self.seed,1,c_r,self.enc_seed)

    def nonzero_count(self,ident):
          """
          Return attributes with count satisfying the threshold
          """
          n=len(ident)
          ans=[]
          for i in range(n):
              d=self.msk.labDecrypt(ident[i])
              if(d==1):
                 ans.append(i)
          return ans

    def decrypt1hotcoding(self,enc_coding,r_start,r_end):
          n=len(enc_coding)
          v=[0 for x in range(n)]
          for i in range(n):
               for j in range(r_start,r_end+1):
                   v[i]+=self.msk.labDecrypt(enc_coding[i][j])
          return v  

