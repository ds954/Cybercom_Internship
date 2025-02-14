# Implement a binary search function binary_search(list, target) that returns the index of the target element in a sorted list, or -1 if the target is not found.


def binary_search(lst,low,high,target_value):
    mid=(low+high)//2
    if target_value==lst[mid]:
        return mid
    if target_value>lst[mid]:
        return binary_search(lst,mid+1,high,target_value)
    elif target_value<lst[mid]:
        return binary_search(lst,low,mid-1,target_value)
    else:
        return -1

lst=[5,7,9,10,11,15,17,20,18,21,25] #20 at index 8
lst=sorted(lst)
target_value=20
high=len(lst)-1
result=binary_search(lst,0,high,target_value)
print("target value at index",result)