#List items are ordered, changeable, and allow duplicate values.

lst=['mango','watermelon','grapes']
lst1=("yellow","red","pink")

#change iteam
lst[1:2]=['blueberry','apple'] #add 2 iteam at the place of watermelon 

#add iteams
lst.insert(3,'strawberry') # insert iteam at specific index
lst.append("fruit") #add at the end of the list
print(lst)
lst.extend(lst1)
print(lst)

#remove iteams
mylist=["red","pink","black","red","blue"]
mylist.remove("red") #remove only first occurence
print(mylist)
mylist.pop(3)# remove index-wise
print(mylist)
mylist.pop()#remove last iteam
print(mylist)
del mylist[1]#remove specified index value
del mylist #remove entier list
print(mylist)
mylist.clear()#only remove iteam return empty list
print(mylist)

#list comprehnsion
lst1=("yellow","red","pink")
newlst=[]

for x in lst1:
    if "e" in x:
        newlst.append(x)
print(newlst)

#same logic using list comprehnsion
newlst=[x for x in lst1 if "e" in x]
print(newlst)

newlist = [x if x != "pink" else "purple" for x in lst1] #if_else condition 
print(newlist)

#sort list
list1= ["banana", "Orange", "Kiwi", "cherry"]
list1.sort()#sort first uppercase iteam 
print(list1)
list1.sort(key=str.lower) #consider all iteam in lower case
print(list1)
list1.sort(reverse=True) 
list1.reverse()
print(list1)

#copy list by 3 way
list1=[5,8,3,9]
list2=[10,15,20]
list3=list2.copy()
list2.append(25)
print(list3)
list4=list(list1)
print(list4)
copylist=list1[:]
print(copylist)