"""
app/calculator.py
Calculator class for performing arithmetic operations
"""

import sys
from typing import List
from app.calculation import Calculation, CalculationFactory

def display_help() -> None:
    """
    Displays help message with usage instructions and supported operations.
    """
    help_message = """
Calculator REPL Help
--------------------
Usage:
    <operation> <number1> <number2>
    - Perform a calculation with the specified operation and two numbers.
    - Supported operations:
        add       : Adds two numbers.
        subtract  : Subtracts the second number from the first.
        multiply  : Multiplies two numbers.
        divide    : Divides the first number by the second.

Special Commands:
    help      : Display this help message.
    history   : Show the history of calculations.
    exit      : Exit the calculator.

Examples:
    add 10 5
    subtract 15.5 3.2
    multiply 7 8
    divide 20 4
    """
    print(help_message)

def display_history(history: List[Calculation]) -> None:
    """
    Displays history of calculations performed during the session.

    Parameters:
        history (List[Calculation]): A list of Calculation objects representing past calculations.
    """
    if not history:
        print("No calculations performed yet.\n")
    else:
        print("Calculation History:")
        for idx, calculation in enumerate(history, start=1):
            print(f"{idx}. {calculation}")
        print("")

def calculator() -> None:
    """REPL calculator that performs addition, subtraction, multiplication, and division."""
    # Initialize an empty list to keep track of calculation history
    history: List[Calculation] = []

    print("Welcome to the calculator REPL! \nType 'help' for instructions or 'exit' to quit.\n")
    
    while True:
        try:
            # Prompt the user to enter an operation and two numbers
            user_input: str = input(">> ").strip()

            # Check for empty input
            if not user_input:
                continue

            # Handle special commands
            command = user_input.lower()

            if command == "help":
                display_help()
                continue
            elif command == "history":
                display_history(history)
                continue
            elif command == "exit":
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
                print("Type 'help' for more information.\n")
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

            # Add calculation to history
            history.append(calculation)

        except KeyboardInterrupt:
            print("\nKeyboard interrupt detected. Exiting calculator. Goodbye!\n")
            sys.exit(0)
        except EOFError:
            print("\nEOF detected. Exiting calculator. Goodbye!\n")
            sys.exit(0)

if __name__ == "__main__":
    calculator()