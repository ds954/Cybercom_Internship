def apply_operation(func, x, y):
    return func(x,y)
def add(a, b):
    return a + b
result_add = apply_operation(add, 5, 3)  
print(f"Addition: {result_add}")  