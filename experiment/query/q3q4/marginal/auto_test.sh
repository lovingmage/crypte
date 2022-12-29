#!/bin/sh

python execute_cr2.py -f testfile.txt -attr1 0 -attr2 1 -Q 3,1,1 -e 0.1 -nd 571
echo " "
python execute_cr2.py -f testfile.txt -attr1 0 -attr2 1 -Q 3,1,1 -e 0.1 -nd 1022
echo " "
python execute_cr2.py -f testfile.txt -attr1 0 -attr2 1 -Q 3,1,1 -e 0.1 -nd 3665
