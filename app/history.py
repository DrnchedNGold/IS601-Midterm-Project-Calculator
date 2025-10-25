# History Management

from abc import ABC, abstractmethod
import logging
from typing import Any
from app.calculation import Calculation


class HistoryObserver(ABC):
    """
    Abstract base class that defines what observers need to implement.

    This is the Observer pattern in action. Observers "watch" the calculator and
    get notified whenever something interesting happens (like a new calculation).
    Each observer can react differently to the same event.
    """

    @abstractmethod
    def update(self, calculation: Calculation) -> None:
        """
        This is the method that the calculator calls to notify the observer.
        Each observer implements this differently based on what it needs to do.

        Args:
            calculation: The calculation that just happened
        """
        pass  # pragma: no cover


class LoggingObserver(HistoryObserver):
    """
    Observer that writes calculation details to the log file.

    It's useful for debugging issues or understanding how the calculator is
    being used.
    """

    def update(self, calculation: Calculation) -> None:
        """
        Logs the calculation details to the log file.

        Args:
            calculation: The calculation to log
        
        Raises:
            AttributeError: If calculation is None (shouldn't happen, but we check)
        """
        if calculation is None:
            raise AttributeError("Calculation cannot be None")
        
        # Write a detailed log entry with all the calculation info
        logging.info(
            f"Calculation performed: {calculation.operation} "
            f"({calculation.operand1}, {calculation.operand2}) = "
            f"{calculation.result}"
        )


class AutoSaveObserver(HistoryObserver):
    """
    Observer that automatically saves history after each calculation.

    This way users don't lose their work if something crashes - the history is
    constantly being saved in the background without them having to think about it.
    """

    def __init__(self, calculator: Any):
        """
        Sets up the observer with a reference to the calculator.

        Args:
            calculator: The calculator instance we're observing
        
        Raises:
            TypeError: If the calculator doesn't have the methods/attributes we need
        """
        # Verify the calculator has what we need before proceeding
        if not hasattr(calculator, 'config') or not hasattr(calculator, 'save_history'):
            raise TypeError("Calculator must have 'config' and 'save_history' attributes")
        self.calculator = calculator

    def update(self, calculation: Calculation) -> None:
        """
        Saves the history if auto-save is enabled.

        Args:
            calculation: The calculation that was just performed
        
        Raises:
            AttributeError: If calculation is None
        """
        if calculation is None:
            raise AttributeError("Calculation cannot be None")
        
        # Only save if auto-save is enabled in the config
        if self.calculator.config.auto_save:
            self.calculator.save_history()
            logging.info("History auto-saved")