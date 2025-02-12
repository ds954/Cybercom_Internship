# scoreatpercentile 
from scipy import stats 
import numpy as np 

# 1D array 
arr = [20, 2, 7, 1, 7, 7, 34, 3] 

print("arr : ", arr) 

print ("\nScore at 50th percentile : ", 
	stats.scoreatpercentile(arr, 50)) 

print ("\nScore at 90th percentile : ", 
	stats.scoreatpercentile(arr, 90)) 

print ("\nScore at 10th percentile : ", 
	stats.scoreatpercentile(arr, 10)) 

print ("\nScore at 100th percentile : ", 
	stats.scoreatpercentile(arr, 100)) 

print ("\nScore at 30th percentile : ", 
	stats.scoreatpercentile(arr, 30)) 
