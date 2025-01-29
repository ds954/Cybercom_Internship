import datetime as dt
x=dt.datetime.now()
print(x)
print(x.strftime("%A")) #return weekday
print(x.strftime("%a")) #return weekday short version
print(x.strftime("%w")) #return weekday as number
print(x.strftime("%d")) #return day of month
print(x.strftime("%b")) #return month short version
print(x.strftime("%B")) #return month
print(x.strftime("%m")) #return month as number
print(x.strftime("%y")) #return year in short
print(x.strftime("%Y")) #return year
print(x.strftime("%H")) #return hour 0-23
print(x.strftime("%I")) #return hour 0-12