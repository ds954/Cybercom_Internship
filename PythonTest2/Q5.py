lst=[1,2,8,6,3,4,7,8]

def filter_even(lst):
    print(list(filter(lambda x: x%2==0,lst)))
filter_even(lst)