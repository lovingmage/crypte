import csv
import time
import numpy as np


from copy import deepcopy
from operator import mul
from AS import AnalyticsServer
from CSP import CSProvider
from DO import DOwner
from QueryEngine import QueryParsing

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

def multi2(intmdt_pro,extra):
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

def evaluate_cp2(inputfile, num_DO,attr1,attr2, Q,e):
    """
    compute 
    :param inputfile : Data file 
    :param num_DOs: the number of Data Owners
    :param Q: Query
    :param e: the privacy budget
    :return : return noisy count for Q
    """
    global mpk, mask
    domain_s=[1,1,20,100]
    domain_e=[2,100,40,120]
    l=3
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
       

    '''Start Secure protocol computation'''
    n_length=2048
	
 

    # declare CSP & MLE & DOwners
    csp = CSProvider()
    As = AnalyticsServer()
    DOwners = []
    for index in range(num_DO):
        DOwners.append(DOwner(D[index],domain_s,domain_e))
   

    #  Parse Query
    Attr,Rstart,Rend=QueryParsing(Q)



    print('Phase 1 : Protocol Laplace-DO')  
    # declare Crypto Service Provider(CSP) & Phase1 step1
    start_P11 = time.time()
    csp.key_gen(n_length)
    end_P11 = time.time()

    # publish public_key to AS & Downers
    mpk=csp.get_MPK()
    As.set_PK(csp.get_MPK())
    for d_owner in DOwners:
        d_owner.set_MPK(csp.get_MPK())    

    # Phase1 step2
    start_P12 = time.time()     
    for d_owner in DOwners:
        d_owner.computeEnc_X()
    end_P12 = time.time()

    # Phase2 Step 1
    print('Phase 2 : Protocol Laplace-AS')
    start_P21 = time.time()
    for d_owner in DOwners:
        enc_Xi = d_owner.getEnc_X()
        #as merges enc_Xi
        As.add_enc_X(enc_Xi,num_DO)
    end_P21 = time.time()



    #aspk=As.getpk()
    #for d_owner in DOwners:
        #pks.append(d_owner.getpk)
    #
    start_P22 = time.time()
   
    enc_X_afterProjection=As.Projection(Attr,l)
    multiplicands=As.Filter(Attr,Rstart,Rend,enc_X_afterProjection)
    if(len(Attr)==1):
       bitTable=[0 for x in range(num_DO)]
       for i in range(num_DO):
         bitTable[i]=multiplicands[i][0]
       flag=0
    else:
    #Generate Bit Table
        intmdt_pro,extra,pks=multi(multiplicands,num_DO)

        intmdt_labPro=csp.generate_labEncProduct(intmdt_pro,pks,num_DO)
    
        while(len(intmdt_labPro)>1 and extra!=[]):
                
                imtmdt_pro,extra,pks=As.multi2(intmdt_labPro,extra,num_DO)

                intmdt_labPro=csp.generate_labEncProduct(intmdt_pro,pks,num_DO)
        n=len(intmdt_labPro)
        for i in range(n):
             for j in range(num_DO):
                 intmdt_labPro[i][j].hm-=mask[i][j]

        bitTable=[ 0 for x in range(num_DO)]
        
        for i in range(num_DO):
          bitTable[i]=intmdt_labPro[0][i]
    #Multiply bitTable with records


    
    pk1,pk2,newTable=As.CrossProduct2(attr1,attr2)
    enc_X_afterProjection=As.ProjectionT(newTable,[l-2],l-1)
    C=csp.generate_labEncProduct22(enc_X_afterProjection,pk1,pk2,num_DO)
    table,pk1,pk2=As.filter_GroupBy(bitTable,C)
    enc_cnt=As.generateEncCount_GroupBy(table)
    C1=As.Laplace_vectorLHE(e,enc_cnt)
    C2=csp.Lap_mul_decrypt2(C1,pk1,pk2,num_DO,e)
    print(C2)
    

    #cnt is the input to the countDistinct SMC    



