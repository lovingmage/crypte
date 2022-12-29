import csv
import time
import numpy as np


from copy import deepcopy
from operator import mul
from AS import AnalyticsServer
from CSP import CSProvider
from DO import DOwner
from QueryEngine import QueryParsing
from QueryEngine import QueryParsing_GroupBy
mask=[]
mpk = None


def multi(multiplicands,num_DO):
    global mask
    s=len(multiplicands[0])
    mask=[[] for x in range(s//2)]
    extra=[]
    if(s%2==1):
       extra=[[] for x in range()]
       for i in range(num_DO):
           extra.append(multiplicands[i][s-1])
    intmdt_pro=[[] for x in range(s//2)]  
    pks=[[]for x in range(s)]    
    for i in range(s//2):
        for j in range(num_DO):
            mask[i].append(np.random.randint(10000,20000))
         
            c=mul(multiplicands[j][i*2],multiplicands[j][i*2+1])
            c+=mask[i][j]
            pks[i*2].append(multiplicands[j][i*2].sigma)
            pks[i*2+1].append(multiplicands[j][i*2+1].sigma)
            intmdt_pro[i].append(c)
    return intmdt_pro,extra,pks

def multi2(intmdt_pro,extra,num_DO):
        global mask,mpk
        n=len(intmdt_pro)
        for i in range(n):
             for j in range(num_DO):
                 intmdt_pro[i][j].hm-=mask[i][j]
        mask=[[] for x in range(n//2+1)]
        intmdt_pro_out=[[] for x in range(n//2 + 1)]
        pks=[[] for x in range(n+2)]
        if(n%2==1 and len(extra) > 0):
             for i in range(self.num_DO):
                 mask[n//2].append(random.randint(10000,20000))
                 temp=mul(extra[i],intmdt_pro[n-1][i])
                 temp+=mpk.encrypt(mask[n//2][i])
                 intmdt_pro_out[n//2].append(temp)
                 pks[n][i]=extra[i].sigma
                 pks[n+1][i]=intmdt_pro[n-1][i].sigma
             extra=[]
        elif(n%2==1 and len(extra)==0):
             for i in range(num_DO):
                 extra.append(intmdt_pro[n-1][i])


        for i in range(n//2):
            for j in range(num_DO):
                temp=mul(intmdt_pro[i*2][j],intmdt_pro[i*2+1][j])
                mask[i].append(random.randint(10000,20000))
                temp=temp+mpk.encrypt(mask[i][j])
                intmdt_pro_out[i].append(temp)
                pks[i*2][j]=intmdt_pro[i*2][j].sigma
                pks[i*2+1][j]=intmdt_pro[i*2+1][j].sigma
        
        return intmdt_pro_out,extra,pks

def evaluate_GroupBy(inputfile, num_DO, Q):
  """
    compute 
    :param inputfile : Data file 
    :param Q: Query
    :return : return noisy count for Q
  """
  global mpk, mask
  domain_s=[1,1,20,100]
  domain_e=[2,100,40,120]
  l=2
  D=[[] for i in range(num_DO)]
  #Generate Dataset

    
  with open(str(inputfile)) as csv_file:
     csv_reader = csv.reader(csv_file, delimiter=',')
     line_count = 0
     i=0    
     for row in csv_reader:
        if(line_count<num_DO):
           D[line_count]=row
           line_count=line_count+1
        else:
           break
       

  n_length=2048
	
 

  # declare CSP & MLE & DOwners
  csp = CSProvider()
  As = AnalyticsServer()
  DOwners = []
  for index in range(num_DO):
        DOwners.append(DOwner(D[index],domain_s,domain_e))
   

    #  Parse Query
  Attr_GB,thresh,flag,flag2,e,count_sym,ec,Attr_Aggr,Aggr,e_Aggr,FilterQ=QueryParsing_GroupBy(Q)
  print("Attr_GB",Attr_GB)
  print("thresh",thresh)
  print("flag",flag)
  print("Flag2",flag2)
  print("e",e)
  print("count_sym",count_sym)
  print("ec",ec)
  print("Attr_Aggr",Attr_Aggr)
  print("Aggr",Aggr)
  print("e_Aggr",e_Aggr) 
  if(FilterQ!='*'):
       print("Filter,",FilterQ)
       Attr,Rstart,Rend=QueryParsing(FilterQ)



  print('Phase 1 : Protocol GroupBy-DO')  
  # declare Crypto Service Provider(CSP) & Phase1 step1
  start_P11 = time.time()
  csp.key_gen(n_length)
  end_P11 = time.time()

  # publish public_key to AS & Downers
  mpk=csp.get_MPK()
  As.set_PK(csp.get_MPK())
  table=As.generate_testvector(32561)
  N=[1000,2500,5000,10000,20000,32561]
  for i in range(6):
     num_DO=N[i]
     r_start=100
     r_end=num_DO-1
     sum=0
     for j in range(10):
         s=time.time()
         c=As.threshold_GroupBy(table,r_end,r_start)
         e=time.time()
         sum=sum+e-s
     print("NUM_DO",num_DO, sum/float(10))
