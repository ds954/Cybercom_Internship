# Write a function find_duplicates(list) that returns a list of all duplicate values from the input list.

lst=[2,4,8,6,5,5,6,4,1,7,8]

def find_duplicates(lst):
    duplicate_num=[]
    for num in range(len(lst)):
        for i in range(num + 1, len(lst)):
            if lst[num]==lst[i]:
                duplicate_num.append(lst[num])
    print(duplicate_num)

find_duplicates(lst)
