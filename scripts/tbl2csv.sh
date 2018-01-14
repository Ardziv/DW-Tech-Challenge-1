#!/usr/bin/env bash

SRCPATH=$1
DSTPATH=$2

for i in ${SRCPATH}/*.tbl; do 
		[ -f "$i" ] || exit 1
		echo "Converting file "$i; 
		j=`basename $i`
		sed 's/|$//' $i > ${DSTPATH}/${j/tbl/csv}; 
done;
