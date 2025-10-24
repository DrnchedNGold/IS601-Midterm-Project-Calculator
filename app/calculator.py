"""
app/calculator.py
Calculator class for performing arithmetic operations
"""
from app.operations import Operations


def calculator():
    """Basic REPL calculator that performs addition, subtraction, multiplication, and division."""
    
    print("Welcome to the calculator REPL! Type 'exit' to quit")
    
    while True:
        # Now we ask the user to type something, like "add 5 3". 
        # This will get the operation (like "add") and two numbers from the user.
        user_input = input("Enter an operation (add, subtract, multiply, divide) and two numbers, or 'exit' to quit: ")

        # This part checks if the user typed "exit". If they did, we print a message and stop the calculator.
        if user_input.lower() == "exit":
            print("Exiting calculator...")
            break

        try:
            # Split input into three parts: the operation (add, subtract, etc.) and the two numbers.
            operation, num1, num2 = user_input.split()
            # Check user input by converting to floats.
            num1, num2 = float(num1), float(num2)
        except ValueError:
            # Throw error if incorect input format is given.
            print("Invalid input. Please follow the format: <operation> <num1> <num2>")
            continue

        # Check what operation the user asked for and call the right function (addition, subtraction, etc.).
        if operation == "add":
            result = Operations.addition(num1, num2)  # We call the correct function.
        elif operation == "subtract":
            result = Operations.subtraction(num1, num2)
        elif operation == "multiply":
            result = Operations.multiplication(num1, num2)
        elif operation == "divide":
            try:
                result = Operations.division(num1, num2)
            except ValueError as e:
                # Handle dividing by zero.
                print(e)  # Print error message.
                continue  # Go back to top and try again.
        else:
            # Handle invalid operation input.
            print(f"Unknown operation '{operation}'. Supported operations: add, subtract, multiply, divide.")
            continue

        print(f"Result: {result}")