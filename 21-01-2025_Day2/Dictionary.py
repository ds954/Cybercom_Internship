#Dictionary items are ordered, changeable, and do not allow duplicates.

# 2 way for create dictionary
mydict={
    'name':'dhara',
    'clg':'vgec',
    'sem':8
}
mydict=dict(name='dhara',clg='vgec',sem=8)


#Access iteam
print(mydict['name'])
print(mydict.get('clg')) #using get() method

print(mydict.keys()) # return all keys
mydict["branch"]="CE" #add key-value pair
print(mydict)

print(mydict.values())#return all values
mydict["branch"]="IT"
print(mydict)

print(mydict.items())#return tuple in list
print(mydict.update({"branch":"CE"})) # can change or add iteams
print(mydict)


#Remove iteams
mydict={
    'name':'dhara',
    'clg':'vgec',
    'sem':8,
    'branch':'CE'
}
print(mydict.pop("sem")) #remove iteam with specified key
print(mydict)
print(mydict.popitem()) #remove last iteams
del mydict["clg"] #remove iteam with specified key
print(mydict)
print(mydict.clear())  #empty dictionary
del mydict #remove entire dictionary


#LOOP in DICT
mydict={
    'name':'dhara',
    'clg':'vgec',
    'sem':8,
    'branch':'CE'
}
for i in mydict:   # return all keys
    print("dict",i)  

for i in mydict: 
    print(mydict[i]) # return all values

for i in mydict.keys():  # return all keys
    print("all keys",i)

for i in mydict.values(): # return all values
    print("all values",i)

for i in mydict.items(): # return all items
    print("items",i)


# copy dict
mydict={
    'name':'dhara',
    'clg':'vgec',
    'sem':8,
    'branch':'CE'
}
mydict1=mydict.copy()
mydict2=dict(mydict)
print(mydict1)
print(mydict2)


#nested Dictionary
GTU={
    'vgec':{
        'name':'abc',
        'branch':'CE'
    },
    'LD':{
        'name':'xyz',
        'branch':'IT'
    }
}

#access in nested dict
print(GTU['LD']['branch'])

for x,obj in GTU.items():
    print(x)

    for y in obj:
        print(y + ':', obj[y])


#other methods

#setbydefault():
mydict={
    'name':'dhara',
    'clg':'vgec',
    'sem':8,
    'branch':'CE'
}
x=mydict.setdefault('sem',7) #return item valur from original dict
print(x)
print(mydict)

#fromkeys():
x=('a','b','c')
y=12
z=dict.fromkeys(x,y) #create dict from tuple
print(z)

y=list(dict.fromkeys(x))
x=[25,63,25,12,2,25,1] #remove duplicates from a List 
print(y)

