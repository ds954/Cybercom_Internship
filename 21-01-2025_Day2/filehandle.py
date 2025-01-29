f=open(r"C:\Users\dsm95\Desktop\Cybercom_Internship\21-01-2025_Day2\textfile.txt",'rt')
print(f.read(10)) # return first 10 char
print(f.readlines())# read line by line
f.close()

#overwrite file
f=open(r"C:\Users\dsm95\Desktop\Cybercom_Internship\21-01-2025_Day2\textfile.txt",'w')
f.write("overwrite the file\n")
f.close()
f=open(r"C:\Users\dsm95\Desktop\Cybercom_Internship\21-01-2025_Day2\textfile.txt",'rt')
print(f.read())

#append 
f=open(r"C:\Users\dsm95\Desktop\Cybercom_Internship\21-01-2025_Day2\textfile.txt",'a')
f.write("append text to the file")
f.close()
f=open(r"C:\Users\dsm95\Desktop\Cybercom_Internship\21-01-2025_Day2\textfile.txt",'rt')
print(f.read())

#remove
import os
if os.path.exists(r"C:\Users\dsm95\Desktop\Cybercom_Internship\21-01-2025_Day2\textfile.txt"):

    os.remove(r"C:\Users\dsm95\Desktop\Cybercom_Internship\21-01-2025_Day2\textfile.txt")
else:
    print("file is not exist")