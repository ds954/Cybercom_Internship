def divide(x, y): 
    try: 
        result = x // y 
    except ZeroDivisionError: 
        # This block executes if a ZeroDivisionError occurs
        print("You are dividing by zero") 
    else:
        # This block executes if no exception occurs
        print("Your answer is:", result) 
    finally:   
        # This block always executes, regardless of whether an exception occurred
        print('This is always executed')   

# Function calls
divide(3, 2)  # Normal division
divide(3, 0)  # Division by zero

