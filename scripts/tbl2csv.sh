#!/usr/bin/env bash

SRCPATH=$1
DSTPATH=$2
for i in `ls ${SRCPATH}/*.tbl`; do 
sed 's/|$//' $i > ${DSTPATH}/${i/tbl/csv}; 
echo $i; 
done;
