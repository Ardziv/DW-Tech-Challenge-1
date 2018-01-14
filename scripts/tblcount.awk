BEGIN { 
	arr[$7]++
} 
END {
	for(i in arr) 
		print i,arr[i]
}
