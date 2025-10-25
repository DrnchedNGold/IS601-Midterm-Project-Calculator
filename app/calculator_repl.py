# Calculator REPL

from decimal import Decimal
import logging

from colorama import Fore, Style, init

from app.calculator import Calculator
from app.exceptions import OperationError, ValidationError
from app.history import AutoSaveObserver, LoggingObserver
from app.operations import OperationFactory

# Initialize colorama for cross-platform colored terminal output
init(autoreset=True)


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
            f"{Fore.CYAN}Welcome to the Python Calculator REPL!{Style.RESET_ALL}\n"
            f"{Fore.YELLOW}Type 'help' for available commands or 'exit' to quit.{Style.RESET_ALL}\n"
            f"{Fore.BLUE}Valid commands: add, subtract, multiply, divide, power, root, modulus, int_divide, percent, abs_diff, history, clear, undo, redo, save, load, help, exit{Style.RESET_ALL}"
        )

        # Main loop - keeps running until the user types 'exit'
        while True:
            try:
                # Get a command from the user and clean it up
                command = input(f"\n{Fore.GREEN}Enter command: {Style.RESET_ALL}").lower().strip()

                if command == 'help':
                    # Show the user what commands are available
                    print(f"\n{Fore.CYAN}Available commands:{Style.RESET_ALL}")
                    print(f"  {Fore.BLUE}add, subtract, multiply, divide, power, root{Style.RESET_ALL} - Basic arithmetic operations")
                    print(f"  {Fore.BLUE}modulus{Style.RESET_ALL} - Calculate remainder of division (a % b)")
                    print(f"  {Fore.BLUE}int_divide{Style.RESET_ALL} - Integer division (floor division)")
                    print(f"  {Fore.BLUE}percent{Style.RESET_ALL} - Calculate percentage (a as percentage of b)")
                    print(f"  {Fore.BLUE}abs_diff{Style.RESET_ALL} - Calculate absolute difference between two numbers")
                    print(f"  {Fore.MAGENTA}history{Style.RESET_ALL} - Show calculation history")
                    print(f"  {Fore.MAGENTA}clear{Style.RESET_ALL} - Clear calculation history")
                    print(f"  {Fore.MAGENTA}undo{Style.RESET_ALL} - Undo the last calculation")
                    print(f"  {Fore.MAGENTA}redo{Style.RESET_ALL} - Redo the last undone calculation")
                    print(f"  {Fore.MAGENTA}save{Style.RESET_ALL} - Save calculation history to file")
                    print(f"  {Fore.MAGENTA}load{Style.RESET_ALL} - Load calculation history from file")
                    print(f"  {Fore.RED}exit{Style.RESET_ALL} - Exit the calculator")
                    continue  # Go back to the start of the loop for the next command

                if command == 'exit':
                    # Try to save history before closing - we don't want to lose work!
                    try:
                        calc.save_history()
                        print(f"{Fore.GREEN}History saved successfully.{Style.RESET_ALL}")
                    except Exception as e:
                        # If saving fails, warn the user but still let them exit
                        print(f"{Fore.YELLOW}Warning: Could not save history: {e}{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}Goodbye!{Style.RESET_ALL}")
                    break  # Exit the loop, ending the program

                if command == 'history':
                    # Show all previous calculations
                    history = calc.show_history()
                    if not history:
                        print(f"{Fore.YELLOW}No calculations in history{Style.RESET_ALL}")
                    else:
                        print(f"\n{Fore.CYAN}Calculation History:{Style.RESET_ALL}")
                        # enumerate gives us both the index and the item
                        for i, entry in enumerate(history, 1):
                            print(f"{i}. {entry}")
                    continue

                if command == 'clear':
                    # Delete all calculations from history
                    calc.clear_history()
                    print(f"{Fore.GREEN}History cleared{Style.RESET_ALL}")
                    continue

                if command == 'undo':
                    # Go back one step in history
                    if calc.undo():
                        print(f"{Fore.GREEN}Operation undone{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.YELLOW}Nothing to undo{Style.RESET_ALL}")
                    continue

                if command == 'redo':
                    # Go forward one step (only works after an undo)
                    if calc.redo():
                        print(f"{Fore.GREEN}Operation redone{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.YELLOW}Nothing to redo{Style.RESET_ALL}")
                    continue

                if command == 'save':
                    # Manually save history to a file
                    try:
                        calc.save_history()
                        print(f"{Fore.GREEN}History saved successfully{Style.RESET_ALL}")
                    except Exception as e:
                        print(f"{Fore.RED}Error saving history: {e}{Style.RESET_ALL}")
                    continue

                if command == 'load':
                    # Load previously saved history from a file
                    try:
                        calc.load_history()
                        print(f"{Fore.GREEN}History loaded successfully{Style.RESET_ALL}")
                    except Exception as e:
                        print(f"{Fore.RED}Error loading history: {e}{Style.RESET_ALL}")
                    continue

                if command in ['add', 'subtract', 'multiply', 'divide', 'power', 'root', 'modulus', 'int_divide', 'percent', 'abs_diff']:
                    # Handle arithmetic operations
                    try:
                        print(f"\n{Fore.YELLOW}Enter numbers (or 'cancel' to abort):{Style.RESET_ALL}")
                        # Get the first number
                        a = input(f"{Fore.GREEN}First number: {Style.RESET_ALL}")
                        if a.lower() == 'cancel':
                            print(f"{Fore.YELLOW}Operation cancelled{Style.RESET_ALL}")
                            continue
                        # Get the second number
                        b = input(f"{Fore.GREEN}Second number: {Style.RESET_ALL}")
                        if b.lower() == 'cancel':
                            print(f"{Fore.YELLOW}Operation cancelled{Style.RESET_ALL}")
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

                        print(f"\n{Fore.GREEN}Result: {Style.BRIGHT}{result}{Style.RESET_ALL}")
                    except (ValidationError, OperationError) as e:
                        # These are expected errors (like dividing by zero)
                        # Show a friendly message without crashing
                        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
                    except Exception as e:
                        # Catch any unexpected errors we didn't anticipate
                        print(f"{Fore.RED}Unexpected error: {e}{Style.RESET_ALL}")
                    continue

                # If we get here, the user typed something we don't recognize
                print(f"{Fore.RED}Unknown command: '{command}'. Type 'help' for available commands.{Style.RESET_ALL}")

            except KeyboardInterrupt:
                # User pressed Ctrl+C - cancel the current operation but keep running
                print(f"\n{Fore.YELLOW}Operation cancelled{Style.RESET_ALL}")
                continue
            except EOFError:
                # User pressed Ctrl+D (or we hit end of input) - exit gracefully
                print(f"\n{Fore.CYAN}Input terminated. Exiting...{Style.RESET_ALL}")
                break
            except Exception as e:
                # Something unexpected happened, but try to keep running
                print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
                continue

    except Exception as e:
        # Something went really wrong during startup - we can't recover
        print(f"{Fore.RED}Fatal error: {e}{Style.RESET_ALL}")
        logging.error(f"Fatal error in calculator REPL: {e}")
        raise  # Re-raise the error so we can see the full traceback
