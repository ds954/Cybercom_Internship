#set is a collection which is unordered, unchangeable, and unindexed.

#add item at set
myset={"python","java","c++","c"}
mylst=["GO","PHP"]
myset.add("Ruby")
myset.update(mylst)
print(myset)

#Remove set
myset={"python","java","c++","c"}
myset.remove("c++") #throw an error if not exits
print(myset)
myset.discard("python") # doesn't throw an error
print(myset)
myset.pop() #randomly del any iteam

#union() set

set1={'a',"b","c"}
set2={"python","java","c++","c"}
print(set1.union(set2))
print(set1|set2) #only allow you set with the set data type
x = {"a", "b", "c"}
y = (1, 2, 3)
print(x.union(y)) #tuple with set,list 

#update()
set1.update(set2)#changes the original set, and does not return a new set.
print(set1) 

#intersection()
set1={'a',"b","c"}
set2={"python","java","c++","c"}
print(set1.intersection(set2))
set3 = set1 & set2 #only allow you set with the set data type
print(set3)
set1.intersection_update(set2)#change the original set instead of returning a new set.
print(set1)

#difference()
set1={'a',"b","c"}
set2={"python","java","c++","c"}
print(set1.difference(set2))
set3 = set1 - set2
print(set3)
set1.difference_update(set2)
print(set1)

#symmetric_difference()
set1={'a',"b","c"}
set2={"python","java","c++","c"}
set3 = set1.symmetric_difference(set2)
print(set3)
set3 = set1 ^ set2
print(set3)
set1.symmetric_difference_update(set2)
print(set1)

#isdisjoint()
set1={'a',"b","c"}
set2={"python","java","c++","c"}
print(set1.isdisjoint(set2)) #Return True if no items in set1 is present in set2.

#issubset()
x = {"a", "b", "c"}
y = {"f", "e", "d", "c", "b", "a"}
z = x.issubset(y) #Return True if all items in set x are present in set y
z = x <= y# short cut
print(z)

#issuperset()
x = {"f", "e", "d", "c", "b", "a"}
y = {"a", "b", "c"}
z = x.issuperset(y)#Return True if all items set y are present in set x
z = x >= y
print(z)