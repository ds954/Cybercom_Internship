#Method1
str=" Hello World! "
ans=str.replace(" ","")
print(ans)


#Method2
str=" Hello@World! "

ans=(str.split('@'))# split first create a list then join 
print(len(ans))
print(ans)


#Method3
str=" Hello World! "
ans="".join(str.strip().split())
print(ans)
