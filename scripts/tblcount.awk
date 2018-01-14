#!/usr/bin/awk -f
{arr[$field_pos]++} END {for(i in arr) print i,arr[i]}
