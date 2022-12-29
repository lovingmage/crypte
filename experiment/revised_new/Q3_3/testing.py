import numpy as np
import math
A=[0 for i in range(10)]
Alog=[0 for i in range(10)]
Mlog=[0 for i in range(10)]
M=[0 for i in range(10)]
S=[0 for i in range(10)]
Slog=[0 for i in range(10)]
m=0
mlog=0
e=0.1
E=[0.1,0.3,0.5,0.7,0.9,1.1,1.3,1.5,1.7,1.9]
for j in range(10):
 e=E[j]
 for i in range(10):
  u=np.random.exponential(1/e)
  v=np.random.exponential(1/e)
  z=u-v
  u=np.random.exponential(1/e)
  v=np.random.exponential(1/e)
  z1=u-v+z
  a=abs(z1)+1
  A[i]=a
  Alog[i]=math.log10(a)
  mlog=mlog+math.log10(a)
  m=m+a
 
 stdlog=np.std(Alog)
 st=np.std(A)
 mlog=mlog/10
 m=m/10
 Slog[j]=stdlog
 S[j]=st
 Mlog[j]=mlog
 M[j]=m

print(Slog)
print(S)
print(Mlog)
print(M)
print("Mean",mlog,m)

