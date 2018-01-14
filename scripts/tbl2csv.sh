#!/usr/bin/env bash

SRCPATH=$1
DSTPATH=$2

for i in ${SRCPATH}/*.tbl; do 
		echo $i; 
		[ -f "$i" ] || exit 1
		j=`basename $i`
		echo $j
		sed 's/|$//' $i > ${DSTPATH}/${j/tbl/csv}; 
done;
