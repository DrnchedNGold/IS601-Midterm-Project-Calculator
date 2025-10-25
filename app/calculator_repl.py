# Calculator REPL

from decimal import Decimal
import logging

from app.calculator import Calculator
from app.exceptions import OperationError, ValidationError
from app.history import AutoSaveObserver, LoggingObserver
from app.operations import OperationFactory


def calculator_repl():
    """
    The main command-line interface for the calculator.

    REPL:
    - Reads input from the user
    - Evaluates (processes) that input
    - Prints the result
    - Loops back to step 1
    """
    try:
        # Create a new calculator instance
        calc = Calculator()

        # Set up observers to automatically log operations and save history
        calc.add_observer(LoggingObserver())
        calc.add_observer(AutoSaveObserver(calc))

        print(
            "Welcome to the Python Calculator REPL!\n"
            "Type 'help' for available commands or 'exit' to quit.\n"
            "Valid commands: add, subtract, multiply, divide, power, root, history, clear, undo, redo, save, load, help, exit"
        )

        # Main loop - keeps running until the user types 'exit'
        while True:
            try:
                # Get a command from the user and clean it up
                command = input("\nEnter command: ").lower().strip()

                if command == 'help':
                    # Show the user what commands are available
                    print("\nAvailable commands:")
                    print("  add, subtract, multiply, divide, power, root - Perform calculations")
                    print("  history - Show calculation history")
                    print("  clear - Clear calculation history")
                    print("  undo - Undo the last calculation")
                    print("  redo - Redo the last undone calculation")
                    print("  save - Save calculation history to file")
                    print("  load - Load calculation history from file")
                    print("  exit - Exit the calculator")
                    continue  # Go back to the start of the loop for the next command

                if command == 'exit':
                    # Try to save history before closing - we don't want to lose work!
                    try:
                        calc.save_history()
                        print("History saved successfully.")
                    except Exception as e:
                        # If saving fails, warn the user but still let them exit
                        print(f"Warning: Could not save history: {e}")
                    print("Goodbye!")
                    break  # Exit the loop, ending the program

                if command == 'history':
                    # Show all previous calculations
                    history = calc.show_history()
                    if not history:
                        print("No calculations in history")
                    else:
                        print("\nCalculation History:")
                        # enumerate gives us both the index and the item
                        for i, entry in enumerate(history, 1):
                            print(f"{i}. {entry}")
                    continue

                if command == 'clear':
                    # Delete all calculations from history
                    calc.clear_history()
                    print("History cleared")
                    continue

                if command == 'undo':
                    # Go back one step in history
                    if calc.undo():
                        print("Operation undone")
                    else:
                        print("Nothing to undo")
                    continue

                if command == 'redo':
                    # Go forward one step (only works after an undo)
                    if calc.redo():
                        print("Operation redone")
                    else:
                        print("Nothing to redo")
                    continue

                if command == 'save':
                    # Manually save history to a file
                    try:
                        calc.save_history()
                        print("History saved successfully")
                    except Exception as e:
                        print(f"Error saving history: {e}")
                    continue

                if command == 'load':
                    # Load previously saved history from a file
                    try:
                        calc.load_history()
                        print("History loaded successfully")
                    except Exception as e:
                        print(f"Error loading history: {e}")
                    continue

                if command in ['add', 'subtract', 'multiply', 'divide', 'power', 'root']:
                    # Handle arithmetic operations
                    try:
                        print("\nEnter numbers (or 'cancel' to abort):")
                        # Get the first number
                        a = input("First number: ")
                        if a.lower() == 'cancel':
                            print("Operation cancelled")
                            continue
                        # Get the second number
                        b = input("Second number: ")
                        if b.lower() == 'cancel':
                            print("Operation cancelled")
                            continue

                        # Use the factory to create the right operation object
                        # This is cleaner than a big if/elif chain
                        operation = OperationFactory.create_operation(command)
                        calc.set_operation(operation)

                        # Do the actual calculation
                        result = calc.perform_operation(a, b)

                        # Clean up the result if it's a Decimal (remove trailing zeros)
                        if isinstance(result, Decimal):
                            result = result.normalize()

                        print(f"\nResult: {result}")
                    except (ValidationError, OperationError) as e:
                        # These are expected errors (like dividing by zero)
                        # Show a friendly message without crashing
                        print(f"Error: {e}")
                    except Exception as e:
                        # Catch any unexpected errors we didn't anticipate
                        print(f"Unexpected error: {e}")
                    continue

                # If we get here, the user typed something we don't recognize
                print(f"Unknown command: '{command}'. Type 'help' for available commands.")

            except KeyboardInterrupt:
                # User pressed Ctrl+C - cancel the current operation but keep running
                print("\nOperation cancelled")
                continue
            except EOFError:
                # User pressed Ctrl+D (or we hit end of input) - exit gracefully
                print("\nInput terminated. Exiting...")
                break
            except Exception as e:
                # Something unexpected happened, but try to keep running
                print(f"Error: {e}")
                continue

    except Exception as e:
        # Something went really wrong during startup - we can't recover
        print(f"Fatal error: {e}")
        logging.error(f"Fatal error in calculator REPL: {e}")
        raise  # Re-raise the error so we can see the full traceback
