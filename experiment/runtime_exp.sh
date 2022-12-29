#!/bin/sh

#Test the running time for q1
#echo "Start Test for q1\n"
#python ./q1q2/range/execute_r2.py -f ./q1q2/range/testfile.txt -attr 1 -r_start 50 -r_end 60 -e 0.1 -nd 3000
#echo "q1-5000-finished.\n\n"

#python ./q1q2/range/execute_r2.py -f ./q1q2/range/testfile.txt -attr 1 -r_start 50 -r_end 60 -e 0.1 -nd 10000
#echo "q1-10000-finished.\n\n"

#python ./q1q2/range/execute_r2.py -f ./q2q2/range/testfile.txt -attr 1 -r_start 50 -r_end 60 -e 0.1 -nd 30000
#echo "q1-30000-finished.\n\n"



#Test the running time for q2
#echo "Start Test for q2\n"
#python ./q1q2/range/execute_r2.py -f ./q1q2/range/testfile.txt -attr 1 -r_start 50 -r_end 60 -e 0.1 -nd 3000
#echo "q2-5000-finished.\n\n"

#python ./q1q2/range/execute_r2.py -f ./q1q2/range/testfile.txt -attr 1 -r_start 50 -r_end 60 -e 0.1 -nd 10000
#echo "q2-10000-finished.\n\n"

#python ./q1q2/range/execute_r2.py -f ./q1q2/range/testfile.txt -attr 1 -r_start 50 -r_end 60 -e 0.1 -nd 30000
#echo "q3-30000-finished.\n\n"

#Test running time for q5
echo "Start Test for q5.\n"
#python ./q5/execute_countD.py -f ./q5/testfile2.txt -attr 1 -Q 0,1,1*3,6,6*1,30,30 -e 0.1 -nd 236
#echo "q5-5000-finished.\n\n"

#python ./q5/execute_countD.py -f ./q5/testfile2.txt -attr 1 -Q 0,1,1*3,6,6*1,30,30 -e 0.1 -nd 371
#echo "q5-10000-finished.\n\n"

#python ./q5/execute_countD.py -f ./q5/testfile2.txt -attr 1 -Q 0,1,1*3,6,6*1,30,30 -e 0.1 -nd 2371
#echo "q5-30000-finished.\n\n"

#Testing running time for q6
echo "Start q6 test.\n"
python execute_countD.py -f testfile.txt -attr 1 -Q 0,1,1 -e 0.1 -nd 236
echo "q6-5000-finished.\n"

python execute_countD.py -f testfile.txt -attr 1 -Q 0,1,1 -e 0.1 -nd 371
echo "q6-10000-finished.\n"

python execute_countD.py -f testfile.txt -attr 1 -Q 0,1,1 -e 0.1 -nd 2371
echo "q6-30000-finished.\n"


#Testing running time for q7
echo "Start q7 test.\n"

