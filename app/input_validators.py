# Author: Varun Sabbineni 10/6/2025
# Input Validation

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Any
from app.calculator_config import CalculatorConfig
from app.exceptions import ValidationError

@dataclass
class InputValidator:
    """
    Handles validating and cleaning up user inputs.
    
    This class makes sure that whatever the user types can actually be used in
    calculations. It checks that inputs are valid numbers, converts them to the
    right format (Decimal for precision), and ensures they're not absurdly large.
    
    We use @dataclass even though we only have static methods because it provides
    a clean namespace for grouping related validation functions together.
    """
    
    @staticmethod
    def validate_number(value: Any, config: CalculatorConfig) -> Decimal:
        """
        Validates user input and converts it to a Decimal for precise calculations.
        
        This method takes whatever the user typed (which could be a string, int,
        float, or already a Decimal) and:
        1. Cleans it up (removes extra whitespace if it's a string)
        2. Converts it to a Decimal (for accurate decimal arithmetic)
        3. Checks that it's not too large (prevents overflow issues)
        4. Normalizes it (removes trailing zeros for cleaner display)
        
        We use Decimal instead of float because floats have precision issues
        with decimal numbers. For example, 0.1 + 0.2 doesn't exactly equal 0.3
        with floats, but it does with Decimal.
        
        Args:
            value: The input to validate (can be string, int, float, or Decimal)
            config: Configuration that tells us the maximum allowed value
            
        Returns:
            Decimal: A validated, normalized Decimal number ready for calculations
            
        Raises:
            ValidationError: If the input isn't a valid number or is too large
        """
        try:
            # If it's a string, clean up any extra whitespace first
            if isinstance(value, str):
                value = value.strip()
            
            # Convert to Decimal - this works for strings, ints, and floats
            # We convert to string first to avoid float precision issues
            number = Decimal(str(value))
            
            # Check if the number is too large (could cause problems)
            if abs(number) > config.max_input_value:
                raise ValidationError(f"Value exceeds maximum allowed: {config.max_input_value}")
            
            # Normalize removes trailing zeros and makes the number cleaner
            # For example, 5.00 becomes 5, and 1.2000 becomes 1.2
            return number.normalize()
            
        except InvalidOperation as e:
            # If Decimal() couldn't convert the value, it's not a valid number
            # Wrap the error in our custom exception with a helpful message
            raise ValidationError(f"Invalid number format: {value}") from e