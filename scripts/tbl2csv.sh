#!/usr/bin/env bash

SRCPATH=$1
DSTPATH=$2
for i in `ls ${SRCPATH}/*.tbl`; do 
j=`basename $i`
echo $j
sed 's/|$//' $i > ${DSTPATH}/${j/tbl/csv}; 
echo $i; 
done;
