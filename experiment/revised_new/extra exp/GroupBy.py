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
  for d_owner in DOwners:
        d_owner.set_MPK(csp.get_MPK())    

    # Phase1 step2
  start_P12 = time.time()  
  i=0   
  for d_owner in DOwners:
        d_owner.computeEnc_X()
        print("DO",i)
        i=i+1
  end_P12 = time.time()

  # Phase2 Step 1
  print('Phase 2 : Protocol GroupBy-AS')
  start_P21 = time.time()
  for d_owner in DOwners:
        enc_Xi = d_owner.getEnc_X()
        #as merges enc_Xi
        As.add_enc_X(enc_Xi,num_DO)
  for i in range(32560):
        As.add_enc_X(enc_Xi,32561)
  end_P21 = time.time()
  start_GB=time.time()


  print("FilterQ",FilterQ)
    


  print("Generate Cipher")
  s1=time.time()
  p=csp.generate_ciphers()
  s2=time.time()
  print("Genrate Cipher S",s2-s1-p)
  #N=[12,4,6,8,10,12]
  N=[32561]
  for i in range(1):
   num_DO=32561
   asSum=0
   as1sum=0
   as2sum=0
   as3sum=0
   as4sum=0
   as5sum=0
   csp1sum=0
   csp2sum=0
   csp3sum=0
   As.set_numDO(num_DO)
   for j in range(10):
    if(FilterQ!='*'):
      enc_X_afterProjection=As.Projection(Attr,l)
      multiplicands=As.Filter(Attr,Rstart,Rend,enc_X_afterProjection)
      if(len(Attr)==1):
        bitTable=[0 for x in range(num_DO)]
        for i in range(num_DO):
          bitTable[i]=multiplicands[i][0]
      else:
      #Generate Bit Table
        intmdt_pro,extra,pks=multi(multiplicands,num_DO)
        intmdt_labPro=csp.generate_labEncProduct(intmdt_pro,pks,num_DO)
    
        while(len(intmdt_labPro)>1 and extra!=[]):
                
                imtmdt_pro,extra,pks=multi2(intmdt_labPro,extra,num_DO)

                intmdt_labPro=csp.generate_labEncProduct(intmdt_pro,pks,num_DO)
        n=len(intmdt_labPro)
        for i in range(n):
             for j in range(num_DO):
                 intmdt_labPro[i][j].hm-=mask[i][j]

        bitTable=[ 0 for x in range(num_DO)]
        
        for i in range(num_DO):
          bitTable[i]=intmdt_labPro[0][i]
    
     
    flaga=0
    startT=time.time()
    #Generate GroupBy Attribute Counts
    as_s=time.time()
    enc_X_after_Projection=As.Projection([Attr_GB],l)
    as_e=time.time()
    if(FilterQ=='*' and Attr_Aggr==[]):
      as1_s=time.time()
      enc_cnt=As.generateEncCount_GroupBy(enc_X_after_Projection)
      as1_e=time.time()
      as2_s=time.time()
      enc_mask_cnt=As.lab_mask_GroupBy(enc_cnt)
      as2_e=time.time()
      csp1_s=time.time()
      mask_cnt=csp.decryptonly(enc_mask_cnt)
      csp1_e=time.time()
      csp2_s=time.time()
      rotate_enc_coding=csp.generateEncCoding2(mask_cnt,num_DO)
      csp2_e=time.time()
    elif(FilterQ=='*' and Attr_Aggr!=[]):
      enc_cnt=As.generateEncNoisyCount_GroupBy(enc_X_after_Projection,ec)
      enc_mask_cnt=As.lab_mask_GroupBy(self,enc_cnt)
      mask_cnt=csp.decryptonly(self,enc_mask_cnt)
      rotate_enc_coding=csp.generateEncNoisyCoding(mask_cnt,num_DO,ec)
    elif(FilterQ!='*' and Attr_Aggr==[]):
      t1=time.time()
      table,pk1,pk2=As.filter_GroupBy(bitTable,enc_X_after_Projection)
      t2=time.time()
      enc_cnt=As.generateEncCount_GroupBy(table)
      t3=time.time()
      enc_mask_cnt=As.mask_GroupBy(enc_cnt)
      t4=time.time()
      mask_cnt=csp.mul_decrypt(enc_mask_cnt,pk1,pk2,num_DO)
      t5=time.time()
      rotate_enc_coding=csp.generateEncCoding2(mask_cnt,num_DO)
      print("done")
      t6=time.time()
    else:
      table,pk1,pk2=As.filter_GroupBy(bitTable,enc_X_after_Projection)
      enc_cnt=As.generateEncNoisyCount_GroupBy(table,ec)
      enc_mask_cnt=As.mask_GroupBy(enc_cnt)
      mask_cnt=csp.mul_decrypt(enc_mask_cnt,pk1,pk2,num_DO)
      rotate_enc_coding=csp.generateEncNoisyCoding(mask_cnt,num_DO,ec)
    
    as3_s=time.time()
    enc_coding=As.rotate_GroupBy(rotate_enc_coding)
    as3_e=time.time()
    #print("Intmdt time,",endT-startT,t6-t5,t5-t4,t4-t3,t3-t2,t2-t1)
    #Count entries satisfying threshold
    if(flag2==0):
          r_start = 0
          r_end = thresh-1
    else:
        r_start = thresh-1
        r_end = num_DO-1
           
    if(flag==1):
      as4_s=time.time()
      enc_count=As.threshold_GroupBy(enc_coding,r_start,r_end) 
      as4_e=time.time()
      as5_s=time.time()
      noisy_enc_count=As.Laplace(enc_count,e)
      as5_e=time.time()
      csp3_s=time.time()
      final_ans=csp.Laplace(noisy_enc_count,e,1)
      csp3_e=time.time()
      flaga=1
    else:
      Enc_attr_thresh=As.noisy_threshold_GroupBy(enc_coding,r_start,r_end)
      attr_thresh=csp.nonzero_count(Enc_attr_thresh) 
      n=len(Attr_Aggr)
      m=len(attr_thresh)
      if(m==0):
         final_ans=0
         m=1
         attr_thresh=[0]
      for i in range(m):
        multiplicands=As.Filter([Attr_GB],[attr_thresh[i]],[attr_thresh[i]],enc_X_afterProjection)
        mask=[]
        pks=[[], []]
        intmdt_pro=[[]]
        for j in range(num_DO):
            mask.append(np.random.randint(10000,20000))

            c=mul(multiplicands[j][0],bitTable[j])
            c+=mpk.encrypt(mask[j])
            pks[0].append(multiplicands[j][0].sigma)
            pks[1].append(bitTable[j].sigma)
            intmdt_pro[0].append(c)
        intmdt_labPro=csp.generate_labEncProduct(intmdt_pro,pks,num_DO)
        for i in range(num_DO):
            intmdt_labPro[0][i].hm-=mask[i]
        As.copy_bitTable(intmdt_labPro)
        for j in range(n):
             encProjection=As.Projection([Attr_Aggr[j]],l)
             intmdt_ans=[[]]
             if(Aggr[j]=='$'):
               #Call count distinct
                enc,pks=As.mult_bit(encProjection)
                intmdt_labPro=csp.generate_labEncProduct(enc,pks,num_DO)
                encount=As.count_distinct(intmdt_labPro)
               # final_ans=callSmc
             else:
                C=As.get_C(j)
                enc,pks=As.mult_bit(encProjection)
                intmdt_labPro=csp.generate_labEncProductT(enc,pks,num_DO)
                intmdt =As.demask(intmdt_labPro)
                s_intmdt,pk1,pk2,mas=As.Sum_Aggregation(intmdt,C)
                s=csp.mul_decrypt_enc(s_intmdt,pk1,pk2)
                
                s-=mas
                intmdt_ans[j].append(s)   
                     
      if(flaga==0):
         final_ans=[[] for x in range(m)]  
      t=[[] for x in range(m)]
      flagt=0
      for i in range(m):
          final_ans[i].append(attr_thresh[i])
          if(count_sym==':'):
             flagt=1
             t[i]=enc_coding[attr_thresh[i]]
      if(flagt):
        c=csp.decrypt1hotcoding(t,r_start,r_end)
        for i in range(m):       
             final_ans[i].append(c[i])
         
      for i in range(n):
          if(Aggr[i]=='+'):
             v=[]
             for j in range(m):
                 v.append(intmdt_ans[j][i])
             v_noisy=As.Laplace_vector(e_Aggr[i],v)
             v=csp.Laplace(v_noisy,e_Aggr[i],m)
             for j in range(m):
                 final_ans[j].append(v[j])
          elif(Aggr[i]=='k'):
             if(flagt==0):
                for i in range(m):
                   t[i]=enc_coding[attr_thresh[i]]
                   c=csp.decrypt1hotcoding(t,r_start,r_end)
             v=[]
             for j in range(m):
                 v.append(intmdt_ans[j][i])     
             v_mask = As.mask(v)
             v_enc=csp.Laplace_avg(v_mask,e_aggr[i],c,m)
             v_tilda=As.demask2(v_tilda,c)
             v=As.Laplace_clear(v_tilda,e_aggr[i],c)
             for j in range(m):
                 final_ans[j].append(v[j])             
          else:
             for j in range(m):
                 final_ans[j].append(intmdt_ans[j][i])


    asSum=asSum+as_e-as_s
    as1sum=as1sum+as1_e-as1_s
    as2sum=as2sum+as2_e-as2_s
    as3sum=as3sum+as3_e-as3_s
    as4sum=as4sum+as4_e-as4_s
    as5sum=as5sum+as5_e-as5_s
    csp1sum=csp1sum+csp1_e-csp1_s
    csp2sum=csp2sum+csp2_e-csp2_s
    csp3sum=csp3sum+csp3_e-csp3_s
    end_GB=time.time()
    #print("Time taken", end_GB-start_GB)
    print(final_ans) 
   print("NUMDO",num_DO)
   print("As-As.projection",asSum/float(10))
   print("As1-AS_generateEncCount_GroupBy",as1sum/float(10))
   print("As2-AS_lab_mask_GroupBy",as2sum/float(10))
   print("As3-AS_rotate_GroupBy",as3sum/float(10))
   print("As4-AS_threshold_GroupBY",as4sum/float(10))
   print("As5_AS_Laplace",as5sum/float(10))
   print("Csp1-CSP_decryptOnly",csp1sum/float(10))
   print("Csp2_CSP_generateEncNoisyCoding",csp2sum/float(10))
   print("Csp3_CSP_Laplace",csp3sum/float(10))
  
  print("Cipher time",s2-s1-p)