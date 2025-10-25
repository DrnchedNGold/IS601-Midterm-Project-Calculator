"""
app/calculator.py
Calculator class for performing arithmetic operations
"""

from decimal import Decimal
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import pandas as pd

from app.calculation import Calculation
from app.calculator_config import CalculatorConfig
from app.calculator_memento import CalculatorMemento
from app.exceptions import OperationError, ValidationError
from app.history import HistoryObserver
from app.input_validators import InputValidator
from app.operations import Operation

# Instead of writing Union[int, float, Decimal] everywhere, we can just say Number
Number = Union[int, float, Decimal]
CalculationResult = Union[Number, str]

class Calculator:
    """
    The main calculator that ties everything together.

    Manages calculations, keeps track of history, handles undo/redo, saves/loads data, and coordinates with observers.
    
    Swappable operations (add, subtract, etc.)
    Notify other components when calculations happen
    Undo/redo functionality
    Factory Pattern: Used by operations to create the right operation type
    """

    def __init__(self, config: Optional[CalculatorConfig] = None):
        """
        Setup calculator with settings
        Args:
            config: Optional configuration object. If None, we use defaults.
        """
        if config is None:
            # Figure out where the project lives so we can set up paths
            current_file = Path(__file__)
            project_root = current_file.parent.parent
            config = CalculatorConfig(base_dir=project_root)

        # Store the config and make sure all settings are valid
        self.config = config
        self.config.validate()

        # Create the directory for log files if it doesn't exist
        os.makedirs(self.config.log_dir, exist_ok=True)

        # Set up the logging system
        self._setup_logging()

        # Initialize empty history and no operation selected yet
        self.history: List[Calculation] = []
        self.operation_strategy: Optional[Operation] = None

        # List of observers watching for new calculations
        self.observers: List[HistoryObserver] = []

        # Stacks for undo/redo - we store snapshots (mementos) of history
        self.undo_stack: List[CalculatorMemento] = []
        self.redo_stack: List[CalculatorMemento] = []

        # Make sure directories for storing history exist
        self._setup_directories()

        try:
            # Try to load any previously saved history
            self.load_history()
        except Exception as e:
            # If loading fails, just warn about it and continue with empty history
            logging.warning(f"Could not load existing history: {e}")

        # Log that we successfully started up
        logging.info("Calculator initialized with configuration")

    def _setup_logging(self) -> None:
        """
        Configures the logging system to write to a file.
        """
        try:
            # Make sure the log directory exists
            os.makedirs(self.config.log_dir, exist_ok=True)
            log_file = self.config.log_file.resolve()

            # Configure Python's logging system
            logging.basicConfig(
                filename=str(log_file),
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s',
                force=True  # Override any existing logging setup
            )
            logging.info(f"Logging initialized at: {log_file}")
        except Exception as e:
            # If we can't set up logging, that's a serious problem
            print(f"Error setting up logging: {e}")
            raise

    def _setup_directories(self) -> None:
        """
        Creates all the directories we need for storing data.
        """
        self.config.history_dir.mkdir(parents=True, exist_ok=True)

    def add_observer(self, observer: HistoryObserver) -> None:
        """
        Registers a new observer to watch for calculations.

        Args:
            observer: The observer object to add to our list
        """
        self.observers.append(observer)
        logging.info(f"Added observer: {observer.__class__.__name__}")

    def remove_observer(self, observer: HistoryObserver) -> None:
        """
        Unregisters an observer so it stops receiving updates.

        Args:
            observer: The observer to remove from our list
        """
        self.observers.remove(observer)
        logging.info(f"Removed observer: {observer.__class__.__name__}")

    def notify_observers(self, calculation: Calculation) -> None:
        """
        Tells all observers that a new calculation happened.

        Args:
            calculation: The calculation that just happened
        """
        for observer in self.observers:
            observer.update(calculation)

    def set_operation(self, operation: Operation) -> None:
        """
        Sets which operation we're going to perform next.

        Args:
            operation: The operation strategy to use
        """
        self.operation_strategy = operation
        logging.info(f"Set operation: {operation}")

    def perform_operation(
        self,
        a: Union[str, Number],
        b: Union[str, Number]
    ) -> CalculationResult:
        """
        Performs a calculation with the current operation strategy.

        Args:
            a: First number
            b: Second number

        Returns:
            Result of calculation

        Raises:
            OperationError: If no operation is set or the calculation fails
            ValidationError: If the inputs aren't valid numbers
        """
        if not self.operation_strategy:
            raise OperationError("No operation set")

        try:
            # Validate and convert inputs to Decimal for precise calculations
            validated_a = InputValidator.validate_number(a, self.config)
            validated_b = InputValidator.validate_number(b, self.config)

            # Use the current operation strategy to calculate the result
            result = self.operation_strategy.execute(validated_a, validated_b)

            # Create a Calculation object to record what we did
            calculation = Calculation(
                operation=str(self.operation_strategy),
                operand1=validated_a,
                operand2=validated_b
            )

            # Save current state to undo stack before making changes
            # This is like taking a snapshot we can restore later
            self.undo_stack.append(CalculatorMemento(self.history.copy()))

            # Clear redo stack because we're creating new history
            # Once you do something new, you can't "redo" the old undone stuff
            self.redo_stack.clear()

            # Add the new calculation to our history
            self.history.append(calculation)

            # Prevent history from growing too large by removing old entries
            if len(self.history) > self.config.max_history_size:
                self.history.pop(0)  # Remove the oldest calculation

            # Let all observers know about the new calculation
            self.notify_observers(calculation)

            return result

        except ValidationError as e:
            # Input validation failed - log it and let the caller handle it
            logging.error(f"Validation error: {str(e)}")
            raise
        except Exception as e:
            # Something unexpected went wrong - wrap it in our exception type
            logging.error(f"Operation failed: {str(e)}")
            raise OperationError(f"Operation failed: {str(e)}")

    def save_history(self) -> None:
        """
        Saves all calculations to a CSV file using pandas.

        Raises:
            OperationError: If something goes wrong while saving
        """
        try:
            # Make sure the directory exists before trying to save
            self.config.history_dir.mkdir(parents=True, exist_ok=True)

            history_data = []
            for calc in self.history:
                # Convert each Calculation to a dictionary for pandas
                history_data.append({
                    'operation': str(calc.operation),
                    'operand1': str(calc.operand1),
                    'operand2': str(calc.operand2),
                    'result': str(calc.result),
                    'timestamp': calc.timestamp.isoformat()
                })

            if history_data:
                # Create a DataFrame and save it to CSV
                df = pd.DataFrame(history_data)
                df.to_csv(self.config.history_file, index=False)
                logging.info(f"History saved successfully to {self.config.history_file}")
            else:
                # If history is empty, create an empty CSV with just the headers
                pd.DataFrame(columns=['operation', 'operand1', 'operand2', 'result', 'timestamp']
                           ).to_csv(self.config.history_file, index=False)
                logging.info("Empty history saved")

        except Exception as e:
            # Log the error and wrap it in our exception type
            logging.error(f"Failed to save history: {e}")
            raise OperationError(f"Failed to save history: {e}")

    def load_history(self) -> None:
        """
        Loads previously saved calculations from a CSV file using pandas.

                Raises:
            OperationError: If something goes wrong while loading
        """
        try:
            if self.config.history_file.exists():
                # Read the CSV into a pandas DataFrame
                df = pd.read_csv(self.config.history_file)
                if not df.empty:
                    # Convert each row back into a Calculation object
                    self.history = [
                        Calculation.from_dict({
                            'operation': row['operation'],
                            'operand1': row['operand1'],
                            'operand2': row['operand2'],
                            'result': row['result'],
                            'timestamp': row['timestamp']
                        })
                        for _, row in df.iterrows()
                    ]
                    logging.info(f"Loaded {len(self.history)} calculations from history")
                else:
                    logging.info("Loaded empty history file")
            else:
                # No history file exists yet - that's fine, we'll create one later
                logging.info("No history file found - starting with empty history")
        except Exception as e:
            # Log the error and wrap it in our exception type
            logging.error(f"Failed to load history: {e}")
            raise OperationError(f"Failed to load history: {e}")

    def get_history_dataframe(self) -> pd.DataFrame:
        """
        Returns the calculation history as a pandas DataFrame.

        Returns:
            DataFrame containing all calculations
        """
        history_data = []
        for calc in self.history:
            history_data.append({
                'operation': str(calc.operation),
                'operand1': str(calc.operand1),
                'operand2': str(calc.operand2),
                'result': str(calc.result),
                'timestamp': calc.timestamp
            })
        return pd.DataFrame(history_data)

    def show_history(self) -> List[str]:
        """
        Returns a list of user-friendly strings showing all calculations.

                Returns:
            List of formatted calculation strings
        """
        return [
            f"{calc.operation}({calc.operand1}, {calc.operand2}) = {calc.result}"
            for calc in self.history
        ]

    def clear_history(self) -> None:
        """
        Deletes all calculations and resets undo/redo stacks.

        Essentially restarting calculator
        """
        self.history.clear()
        self.undo_stack.clear()
        self.redo_stack.clear()
        logging.info("History cleared")

    def undo(self) -> bool:
        """
        Undoes the last calculation by restoring a previous state.

        Returns:
            True if we undid something, False if there was nothing to undo
        """
        if not self.undo_stack:
            return False
        
        # Get the previous state from the undo stack
        memento = self.undo_stack.pop()
        
        # Save current state to redo stack in case user wants to redo
        self.redo_stack.append(CalculatorMemento(self.history.copy()))
        
        # Restore the history from the memento
        self.history = memento.history.copy()
        return True

    def redo(self) -> bool:
        """
        Redoes a previously undone calculation.

        Returns:
            True if we redid something, False if there was nothing to redo
        """
        if not self.redo_stack:
            return False
        
        # Get the state to restore from the redo stack
        memento = self.redo_stack.pop()
        
        # Save current state to undo stack
        self.undo_stack.append(CalculatorMemento(self.history.copy()))
        
        # Restore the history from the memento
        self.history = memento.history.copy()
        return True
