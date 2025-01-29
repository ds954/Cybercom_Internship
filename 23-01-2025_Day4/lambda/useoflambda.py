# 1. Simple Arithmetic
add = lambda x, y: x + y
print("1. Add:", add(5, 3))  # Output: 8

# 2. Sorting a List of Tuples
data = [(1, 'B'), (3, 'A'), (2, 'C')]
sorted_data = sorted(data, key=lambda x: x[1])
print("2. Sorted Data:", sorted_data)  # Output: [(3, 'A'), (1, 'B'), (2, 'C')]

# 3. Filter with Lambda
nums = [1, 2, 3, 4, 5, 6]
evens = list(filter(lambda x: x % 2 == 0, nums))
print("3. Even Numbers:", evens)  # Output: [2, 4, 6]

# 4. Map with Lambda
squared = list(map(lambda x: x ** 2, nums))
print("4. Squared Numbers:", squared)  # Output: [1, 4, 9, 16, 25, 36]



# 5. Conditional Expressions
check_even_odd = lambda x: "even" if x % 2 == 0 else "odd"
print("5. Check Even or Odd:", check_even_odd(7))  # Output: odd
print("5. Check Even or Odd:", check_even_odd(8))  # Output: even

# 6. Lambda in Function Arguments
words = ['apple', 'banana', 'cherry']
longest_word = max(words, key=lambda word: len(word))
print("6. Longest Word:", longest_word)  # Output: banana

# 7. Using Lambda in List Comprehensions
squared_numbers = [(lambda x: x ** 2)(x) for x in range(5)]
print("7. Squared Numbers Using List Comprehension:", squared_numbers)  # Output: [0, 1, 4, 9, 16]
