import random
file=open("testfile2.txt","w")
num_DO=1000000
for i in range(num_DO):
	s1=random.randint(1,2)
	s2=random.randint(1,10)
	s3=random.randint(20,25)
	s4=random.randint(10,12)
	s=str(s1)+","+str(s2)+","+str(s3)+","+str(s4)+"\n"
	file.write(s)
file.close()

