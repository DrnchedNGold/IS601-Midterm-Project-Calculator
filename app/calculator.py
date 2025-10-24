"""
app/calculator.py
Calculator class for performing arithmetic operations
"""

import sys
from app.calculation import Calculation, CalculationFactory

def calculator() -> None:
    """REPL calculator that performs addition, subtraction, multiplication, and division."""
    
    print("Welcome to the calculator REPL! Type 'exit' to quit")
    
    while True:
        try:
            # Prompt the user to enter an operation and two numbers
            user_input: str = input(">> ").strip()

            # Check for empty input
            if not user_input:
                continue

            # Handle special commands
            command = user_input.lower()

            if command == "exit":
                print("Exiting calculator. Goodbye!\n")
                sys.exit(0)

            try:
                # Split input into three parts: the operation and the two numbers.
                operation, num1_str, num2_str = user_input.split()
                # Check user input by converting to floats.
                num1: float = float(num1_str)
                num2: float = float(num2_str)
            except ValueError:
                # Throw error if incorect input format is given.
                print("Invalid input. Please follow the format: <operation> <num1> <num2>")
                continue
            
            # Attempt to create a Calculation instance using the factory
            try:
                calculation = CalculationFactory.create_calculation(operation, num1, num2)
            except ValueError as ve:
                # Handle unsupported operations
                print(ve)
                print("Type 'help' to see the list of supported operations.\n")
                continue  # Prompt the user again

            # Attempt to execute the calculation
            try:
                result = calculation.execute()
            except ZeroDivisionError:
                # Handle division by zero specifically
                print("Cannot divide by zero.")
                print("Please enter a non-zero divisor.\n")
                continue  # Prompt the user again
            except Exception as e:
                # Handle any other unforeseen exceptions
                print(f"An error occurred during calculation: {e}")
                print("Please try again.\n")
                continue  # Prompt the user again

            # Prepare the result string for display
            result_str: str = f"{calculation}"
            print(f"Result: {result_str}\n")

        except KeyboardInterrupt:
            print("\nKeyboard interrupt detected. Exiting calculator. Goodbye!\n")
            sys.exit(0)
        except EOFError:
            print("\nEOF detected. Exiting calculator. Goodbye!\n")
            sys.exit(0)

if __name__ == "__main__":
    calculator()