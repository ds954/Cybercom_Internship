arr=[3.14589,7.14654,8.12345]
round_arr=[(lambda x: round(x, 2))(num) for num in arr]
print(round_arr)