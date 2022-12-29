import random
import time
import math
import numpy as np
import multiprocessing as multi
from copy import deepcopy 
from operator import mul
from itertools import chain
from tree import Tree
from labScheme import localGen



#Analytics Server
class AnalyticsServer:
    def __init__(self):
        self.mpk = None
        self.merged_enc_X = []
        self.l=2
        self.num_DO=None
        self.domain_s=[1,1,20,10]
        self.domain_e=[2,100,25,12]
        self.domain_size=[2,100,5,2]
        self.range_root=None
        self.c=0
        self.noisy_range_root=None
        self.Y=[]
        self.M=[[]]
        self.bitTable=[]
        self.mask=[]
    '''	
    def set_dict(self):
        self.range[0]=0
        for i in range(1,self.l):
            self.range[i]=self.range[i-1]+self.domain_e[i-1]-self.domain_s[i-1]+1
	''' 	
    
    def set_PK(self, pk):
        self.mpk = pk
        self.seed,self.enc_seed=localGen(pk)


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
        
    def initialise_bittable(self):
        """
        Set bit values to 1 before very query
        """

        self.bitTable=[[] for x in range(self.num_DO)]
        for i in range(self.num_DO):
            t=self.mpk.labEncrypt(self.seed,1,1,self.enc_seed)
            self.bitTable[i].append(t)



    def compute_index(self,attribute,value):
	#computes the index that represents the 
        ind=self.range[attribute]+value-self.domain_s[attribute]
        return ind

    def Projection(self,attribute,record_size):
        """
        Perform projection to retain only one-hot-codings for the attributes in 'attribute'
        Param:db- Input database
              record_size- number of attributes per record
        """
        enc_X_afterProjection=[]
        db=self.merged_enc_X
        for i in range(self.num_DO):
            for j in range(len(attribute)):
                enc_X_afterProjection.append(db[i*record_size+attribute[j]])
        return enc_X_afterProjection


    def Filter(self,Attr,r_start,r_end,enc_X_afterProjection):
        """
        Filter out irrelevant values from the one-hot-coding
        Param: enc_X_after_projection-projected input table
               Attr- Attributes in conjunction
               r_start- start of range for each attribute in Attr
               r_end - end of range for each attribute in Attr
        Return:bitTable- bit indicators for each record
        """
        enc_X_afterProjection_Filter=[[] for x in range(self.num_DO)]
        size=len(Attr)
        multiplicands=[[] for x in range(self.num_DO)]
        for i in range(self.num_DO):
            for j in range(size):
                ind1=r_start[j]-self.domain_s[Attr[j]]
                ind2=r_end[j]-self.domain_s[Attr[j]]
                c=0
                for k in range(ind1,ind2+1):
                    c=c+enc_X_afterProjection[i*(size)+j][k]

                multiplicands[i].append(c)  
       # for i in range(self.num_DO):
       #      multiplicands[i].append(self.bitTable[i])       
        return multiplicands

    
    def count(self,bitTable):
        """
        Counts all the valid records satisfying the query at hand
        """
        
        sum=0
        for i in range(self.num_DO):
            sum+=bitTable[i]

        return sum
        
    def copy_bitTable(self,copy):
        self.bitTable=[]
        if(len(copy)==self.num_DO and len(copy[0])==1):
          for i in range(self.num_DO):
             self.bitTable.append(copy[i][0])
        elif(len(copy)==1):
            for i in range(self.num_DO):
             self.bitTable.append(copy[0][i])
        else:
             
             self.bitTable=copy

    def Laplace(self,c,e):
        '''
                        Protocol-Laplace Step1(data masking)
        - Aggregate the data to find the encrypted count
	- Add encrypted noise
	:para attribute, r_start,r_end: the count of records satisfying attribute with value from r_start to r_end is being computed 
	:para e : privacy budget epsilon
        :return enc_Ctilda: Enc(Ctilda) = Enc(count)+Enc(noiseAS)
        '''
        
        u=np.random.geometric(1-math.exp(-e))
        v=np.random.geometric(1-math.exp(-e))
        z=u-v
        enc_z=self.mpk.labEncrypt(self.seed,1,z,self.enc_seed)
        c+=enc_z
        enc_Ctilda=[]
        enc_Ctilda.append(c)
        
        return enc_Ctilda
    
    
    def range_tree(self,attr):
        """
        Compute the range tree
        """
        count_leaves=[0 for x in range(self.domain_size[attr])]
        for i in range(self.num_DO):
             for j in range(self.domain_size[attr]):
                 count_leaves[j]+=self.merged_enc_X[i*self.l+attr][j]
        root=Tree()
        root.data=self.mpk.labEncrypt(self.num_DO,self.seed,1,self.enc_seed)
        leaf=[Tree() for x in range(self.domain_size[attr])]
        for i in range(self.domain_size[attr]):
            leaf[i].data=count_leaves[i]
            leaf[i].lrs=i+1
            leaf[i].lre=i+1
            leaf[i].rre=i+1
            leaf[i].rrs=i+1
        temp=leaf[:]
        while(len(temp)>1):
             temp2=[]
             for i in range(0,len(temp),2):
                 
                 t=Tree()
                 if(i<len(temp)-1):
                   t.data=temp[i].data+temp[i+1].data
                   t.lrs=temp[i].lrs
                   t.lre=temp[i].rre
                   t.rrs=temp[i+1].lrs
                   t.rre=temp[i+1].rre
                   t.left=temp[i]
                   t.right=temp[i+1]
                 else:
                   t=temp[-1]
                   del temp[-1]
                   
                 
                 temp2.append(t)
             temp=temp2[:]
        self.range_root=temp[0]
    
    def range_qhelper(self,node,v1,v2):
         """
         Answer range queries using the range tree
         param: v1 - start of the range
                v2 - end of the range
         """
         count=0
         self.c=self.c+1
         if(v1==node.lrs and v2==node.rre):
                   count=node.data
                   return count
         if(v1>=node.lrs and v2<=node.lre):
                   node=node.left
                   count=self.range_qhelper(node,v1,v2)
         elif(v1>=node.rrs and v2<=node.rre):
                   node=node.right
                   count=self.range_qhelper(node,v1,v2)
         elif(v1>=node.lrs and v2<=node.rre):
                   count+=self.range_qhelper(node.left,v1,node.lre)
                   count+=self.range_qhelper(node.right,node.lre+1,v2)
         elif(v1==node.lrs and v2==node.rre):
                   count=node.data
                   return count
         return count

    def construct_noisyRangeTree(self,e):
        """
        constructing the Noisy Range tree
        """
        self.noisy_range_root=Tree()
        self.addnoise(self.range_root,self.noisy_range_root,e)
    def addnoise(self,root,nroot,e):
        """
        Add noise to the counts 
        """
        if(root==None):
           return
        u=np.random.geometric(1-math.exp(-e))
        v=np.random.geometric(1-math.exp(-e))
        z=u-v
        enc_z=self.mpk.labEncrypt(self.seed,1,z,self.enc_seed)
        nroot.data=enc_z+root.data
        nroot.left=root.left
        nroot.right=root.right
        nroot.lre=root.lre
        nroot.lrs=root.lrs
        nroot.rre=root.rre
        nroot.rrs=root.rrs
        self.addnoise(root.left,nroot.left,e)
        self.addnoise(root.right,nroot.right,e)
        return



    def range_q(self,v1,v2):
         """
         Answer range queries using the range tree
         """
         count=self.range_qhelper(self.range_root,v1+1,v2)
         count1=self.range_qhelper(self.noisy_range_root,v1+1,v2)
         return(count1,count)
    '''
    def inf_range(self,root,flag):
          """Inference"""
          #Constructing Y
          if(root==None):
              return
          if(flag==1):
               self.Y.append(root.data)
               self.l=[1 for x in range(size_attr)]
               self.M.append(l)
          self.inf_range(root.left,1)
          self.inf_range(root.right,0)
          '''

    def noise_Y(self,e):
         l=len(self.Y)
         for i in range(l):
              u=np.random.geometric(1-pow(2.713,-e))
              v=np.random.geometric(1-pow(2.713,-e))
              z=u-v
              enc_z=self.pk.encrypt(z)
              self.Y[i]+=enc_z
   #def noisy_rangetree(self,attr,e):
       
    def filter_GroupBy(self,bitTable,table):
       """
       Uses 
       """
       ans=[[] for i in range(self.num_DO)]
       pk1=[[] for i in range(self.num_DO)]
       pk2=[[] for i in range(self.num_DO)]
       n=len(table[0])
       for i in range(self.num_DO):
           for j in range(n):
               tt=time.time()
               v=mul(table[i][j],bitTable[i])
               tto=time.time()
               print("MUL time", tto-tt)
               pk1[i].append(table[i][j].sigma)
               pk2[i].append(bitTable[i].sigma)
               ans[i].append(v)     
       return  ans,pk1,pk2
   
    
    def generateEncCount_GroupBy(self,table):
        """
        """
        
        n=len(table[0])
        cnt=[0 for x in range(n)]  
        for i in range(self.num_DO):
            for j in range(n):
                cnt[j]+=table[i][j]
        return cnt


    def generateEncNoisyCount_GroupBy(self,table,e):
        """
        """

        n=len(table[0])
        cnt=[0 for x in range(n)]
        for i in range(self.num_DO):
            for j in range(n):
                cnt[j]+=table[i][j]
        

        for i in range(n):
              u=np.random.geometric(1-pow(2.713,-e))
              v=np.random.geometric(1-pow(2.713,-e))
              z=u-v
              enc_z=self.mpk.labEncrypt(self.seed,1,z,self.enc_seed)
              cnt[i]+=enc_z
        return cnt



    def lab_mask_GroupBy(self,cnt):
        """
        Masks the values of the encrypted count before sending for decryption
        Param: cnt - The vector of encrypted counts
        Return: masked_cnt- Masked vector of encrypted counts
        """
        self.mask=[]
        for i in range(n):
            self.mask.append(np.random.randint(self.num_DO))
            enc_mask=self.mpk.labEncrypt(self.seed,1,self.mask[i],self.enc_seed)
            cnt[i]+=enc_mask
        return cnt

    def mask_GroupBy(self,cnt):
        self.mask=[]
        n=len(cnt)
        for i in range(n):
            self.mask.append(np.random.randint(self.num_DO))
            enc_mask=self.mpk.encrypt(self.mask[i])
            cnt[i]+=enc_mask
        return cnt
    
    def rotate_GroupBy(self,in_table):
       """
       Remove the extraneous bits to generate the correct 1-hot-coding
       Param: in_table - output of CSP for Group By
       Return: Table  - 
       """
       n=len(in_table)
       Table=[[] for x in range(n)]
       for i in range(n):
           Table[i]=self.rotate(in_table[i],self.mask[i])
       return Table
    def rotate(self,row,val):
        """
        Rotates the row by val
        """
        if(row==None):
          return
        n = len(row)
        a= n - val
        row=self.reverse(row,0,a-1)
        row=self.reverse(row,a,n-1)
        row=self.reverse(row, 0, n-1)
        return row
    
    def reverse(self,row,left,right):
        if(row == [] or row == None or len(row) == 1): 
            return
        while(left < right):
            temp = row[left]
            row[left] = row[right]
            row[right] = temp
            left=left+1
            right=right-1
        return row
    
    def post_groupBy_threshold(self,table,r_start,r_end,C):
        """
        Param: table - Output of Group By ckt
               r_start,r_end - count in [r_start,r_end]
        """
        n=len(table)
        ans=[]
        for i in range(n):
            v=0
            for j in range(r_start,r_end+1):
                v=v+table[j]
            ans.append(mul(v,C[i]))
        return ans

    def generic_count(self, table):
        """
        Generalised implementation of count primitive
        """
        n=len(table)
        v=0
        for i in range(n):
           v=v+table[i]
 
        return v
    
    def threshold_GroupBy(self,enc_coding,hi,lo):
        """
        Return group by table satisfying
        """
        n=len(enc_coding)
        sum=0
        for i in range(n):
            for j in range(lo,hi):
                sum+=enc_coding[i][j]
        return sum
             
    def one_hot_coding_toVal(self,coding):
        """
        Convert 1 hot coding of counts to
        """
        n=len(coding)
        pk1=[[] for x in range(n)]
        pk2=[[] for x in range(n)]
        val=[]
        for i in range(n):
            sum=0
   
            for j in range(self.num_DO):
                cipher1=self.mpk.labEncrypt(self.seed,1,j+1,self.enc_seed)
                pk1[i].append(cipher1.sigma)
                pk2[i].append(coding[i][j].sigma)
                v=mul(cipher1*coding[i][j])
                sum+=v
            val.append(sum)
        return val,pk1,pk2
    def Laplace_vector(self,e,C):
        n=len(C)
        for i in range(n):
              u=np.random.geometric(1-pow(2.713,-e))
              v=np.random.geometric(1-pow(2.713,-e))
              z=u-v
              enc_z=self.mpk.labEncrypt(self.seed,1,z,self.enc_seed)
              C[i]+=enc_z
        return C
    
    def getpk(self):
        return self.mpk.encrypt(self.seed)

    def noisy_threshold_GroupBy(self,enc_coding,lo,hi):
        """
        Return group by table satisfying
        """
        
        n=len(enc_coding)
        ident=[]
        for i in range(n):
            sum=0
            for j in range(lo,hi):
                sum=enc_coding[i][j]+sum
            ident.append(sum)
        return ident
    
    def get_C(self,attr):
        """
        Get encrypted C
        """ 
        n=self.domain_e[attr]-self.domain_s[attr]+1
        C=[]
        for i in range(n):
            C.append(self.mpk.labEncrypt(self.seed,1,self.domain_s[attr]+i,self.enc_seed))

        return C
    
    def mult_bit(self,encProjection):
         n=len(encProjection[0])
         self.mask=[[] for x in range(self.num_DO)]
         encMult=[[] for x in range(self.num_DO)]
         pk1=[[]for x in range(2*self.num_DO)]
         for i in range(self.num_DO):
             for j in range(n):
                 encMult[i].append(mul(self.bitTable[i],encProjection[i][j]))
                 self.mask[i].append(random.randint(10000,20000))
                 encMult[i][j]+=self.mpk.encrypt(self.mask[i][j])
                 pk1[i*2].append(encProjection[i][j].sigma)
                 pk1[i*2+1].append(self.bitTable[i].sigma)
         return encMult,pk1
     
    def demask(self,table):
         n=len(table[0])
         for i in range(self.num_DO):
             for j in range(n):
                 table[i][j].hm-=self.mask[i][j]
         return table
             
    def mask(self,table):
         self.mask=[]
         n=len(table)
         for i in range(n):
              self.mask.append()
              table[i]+=self.mpk.labEncrypt()
              
    def demask2(self,table,c):
         n=len(table)
         for i in range(n):
             table[i]-=self.mask[i]/c[i]
         return table
     
    def Laplace_clear(self,table,e,c):
         n=len(table) 
         for i in range(n):
             u=np.random.geometric(1-pow(2.713,-e/c[i]))
             v=np.random.geometric(1-pow(2.713,-e/c[i]))
             z=u-v
             table[i]+=z
                 

         return table
    def Sum_Aggregation(self,enc_after_projection,C):
         n=len(C)
         
         pk1=[[]for x in range(self.num_DO)]
         pk2=[[]for x in range(self.num_DO)]
         sum=0
         for i in range(self.num_DO):
             for j in range(n):
                sum+=mul(enc_after_projection[i][j],C[j])
                pk1[i].append(enc_after_projection[i][j].sigma)
                pk2[i].append(C[j].sigma)
         g=np.random.randint(100,200)
         genc=self.mpk.labEncrypt(self.seed,1,g,self.enc_seed)
         return sum+g,pk1,pk2,genc
    def count_distinct(self,table):
         n=len(table[0])
         v=[0 for x in range(n)]
         for i in range(self.num_DO):
             for j in range(n):
                 v[j]+=table[i][j]
         return v
