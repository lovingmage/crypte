#!/bin/bash

python execute_countD.py -f testfile.txt -attr 1 -Q 0,1,1*3,6,6*1,30,30 -e 0.1 -nd 634
echo " "
echo "=========>"
python execute_countD.py -f testfile.txt -attr 1 -Q 0,1,1*3,6,6*1,30,30 -e 0.1 -nd 708
echo " "
echo "=========>"
python execute_countD.py -f testfile.txt -attr 1 -Q 0,1,1*3,6,6*1,30,30 -e 0.1 -nd 715
echo " "
echo "=========>"
python execute_countD.py -f testfile.txt -attr 1 -Q 0,1,1*3,6,6*1,30,30 -e 0.1 -nd 724
echo " "
echo "=========>
python execute_countD.py -f testfile.txt -attr 1 -Q 0,1,1*3,6,6*1,30,30 -e 0.1 -nd 1000
