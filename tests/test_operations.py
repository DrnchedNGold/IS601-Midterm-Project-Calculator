""" 
tests/test_operations.py 
"""

import pytest
from typing import Union  # Import Union for type hinting multiple possible types
from app.operations import Operations  # Import Operations class from operations module

# Define a type alias for numbers that can be either int or float
Number = Union[int, float]

# ========================================
# Unit Tests for 'addition' Method
# ========================================

@pytest.mark.parametrize(
    "a, b, expected",
    [
        (2, 3, 5),           # Test adding two positive integers
        (0, 0, 0),           # Test adding two zeros
        (-1, 1, 0),          # Test adding a negative and a positive integer
        (2.5, 3.5, 6.0),     # Test adding two positive floats
        (-2.5, 3.5, 1.0),    # Test adding a negative float and a positive float
    ],
    ids=[
        "add_two_positive_integers",
        "add_two_zeros",
        "add_negative_and_positive_integer",
        "add_two_positive_floats",
        "add_negative_float_and_positive_float",
    ]
)
def test_addition(a: Number, b: Number, expected: Number) -> None:
    """
    Test 'addition'

    Parameters:
    - a (Number): The first number to add.
    - b (Number): The second number to add.
    - expected (Number): The expected result of the addition.

    Steps:
    1. Call the 'addition' method with arguments 'a' and 'b'.
    2. Assert that the result is equal to 'expected'.

    Examples:
    >>> test_addition(2, 3, 5)
    >>> test_addition(-1, 1, 0)
    """
    # Create instance of Operations class and call addition method
    result = Operations.addition(a, b)
    
    # Assert that the result of addition(a, b) matches the expected value
    assert result == expected, f"Expected addition({a}, {b}) to be {expected}, but got {result}"

# ========================================
# Unit Tests for 'subtraction' Method
# ========================================

@pytest.mark.parametrize(
    "a, b, expected",
    [
        (5, 3, 2),           # Test subtracting a smaller positive integer from a larger one
        (0, 0, 0),           # Test subtracting two zeros
        (-5, -3, -2),        # Test subtracting a negative integer from another negative integer
        (10.5, 5.5, 5.0),    # Test subtracting two positive floats
        (-10.5, -5.5, -5.0), # Test subtracting two negative floats
    ],
    ids=[
        "subtract_smaller_positive_integer_from_larger",
        "subtract_two_zeros",
        "subtract_negative_integer_from_negative_integer",
        "subtract_two_positive_floats",
        "subtract_two_negative_floats",
    ]
)
def test_subtraction(a: Number, b: Number, expected: Number) -> None:
    """
    Test 'subtraction'.

    Parameters:
    - a (Number): The number from which to subtract.
    - b (Number): The number to subtract.
    - expected (Number): The expected result of the subtraction.

    Steps:
    1. Call the 'subtraction' method with arguments 'a' and 'b'.
    2. Assert that the result is equal to 'expected'.

    Examples:
    >>> test_subtraction(5, 3, 2)
    >>> test_subtraction(-5, -3, -2)
    """
    result = Operations.subtraction(a, b)
    
    assert result == expected, f"Expected subtraction({a}, {b}) to be {expected}, but got {result}"

# ========================================
# Unit Tests for 'multiplication' Method
# ========================================

@pytest.mark.parametrize(
    "a, b, expected",
    [
        (2, 3, 6),           # Test multiplying two positive integers
        (0, 10, 0),          # Test multiplying zero with a positive integer
        (-2, -3, 6),         # Test multiplying two negative integers
        (2.5, 4.0, 10.0),    # Test multiplying two positive floats
        (-2.5, 4.0, -10.0),  # Test multiplying a negative float with a positive float
    ],
    ids=[
        "multiply_two_positive_integers",
        "multiply_zero_with_positive_integer",
        "multiply_two_negative_integers",
        "multiply_two_positive_floats",
        "multiply_negative_float_with_positive_float",
    ]
)
def test_multiplication(a: Number, b: Number, expected: Number) -> None:
    """
    Test 'multiplication'

    Parameters:
    - a (Number): The first number to multiply.
    - b (Number): The second number to multiply.
    - expected (Number): The expected result of the multiplication.

    Steps:
    1. Call the 'multiplication' method with arguments 'a' and 'b'.
    2. Assert that the result is equal to 'expected'.

    Examples:
    >>> test_multiplication(2, 3, 6)
    >>> test_multiplication(-2, -3, 6)
    """    
    result = Operations.multiplication(a, b)
    
    assert result == expected, f"Expected multiplication({a}, {b}) to be {expected}, but got {result}"

# ========================================
# Unit Tests for 'division' Method
# ========================================

@pytest.mark.parametrize(
    "a, b, expected",
    [
        (6, 3, 2.0),           # Test dividing two positive integers
        (-6, -3, 2.0),         # Test dividing two negative integers
        (6.0, 3.0, 2.0),       # Test dividing two positive floats
        (-6.0, 3.0, -2.0),     # Test dividing a negative float by a positive float
        (0, 5, 0.0),            # Test dividing zero by a positive integer
    ],
    ids=[
        "divide_two_positive_integers",
        "divide_two_negative_integers",
        "divide_two_positive_floats",
        "divide_negative_float_by_positive_float",
        "divide_zero_by_positive_integer",
    ]
)
def test_division(a: Number, b: Number, expected: float) -> None:
    """
    Test 'division'

    Parameters:
    - a (Number): The dividend.
    - b (Number): The divisor.
    - expected (float): The expected result of the division.

    Steps:
    1. Call the 'division' method with arguments 'a' and 'b'.
    2. Assert that the result is equal to 'expected'.

    Examples:
    >>> test_division(6, 3, 2.0)
    >>> test_division(-6, 3, -2.0)
    """
    result = Operations.division(a, b)

    assert result == expected, f"Expected division({a}, {b}) to be {expected}, but got {result}"

# ===================================================
# Negative Test Case: Division by Zero
# ===================================================

@pytest.mark.parametrize(
    "a, b",
    [
        (1, 0),    # Test dividing by zero with positive dividend
        (-1, 0),   # Test dividing by zero with negative dividend
        (0, 0),    # Test dividing zero by zero
    ],
    ids=[
        "divide_positive_dividend_by_zero",
        "divide_negative_dividend_by_zero",
        "divide_zero_by_zero",
    ]
)
def test_division_by_zero(a: Number, b: Number) -> None:
    """
    Test 'division' when dividing by zero.

    Parameters:
    - a (Number): The dividend.
    - b (Number): The divisor (zero in this case).

    Steps:
    1. Attempt to call the 'division' method with arguments 'a' and 'b', which should raise a ValueError.
    2. Use pytest's 'raises' context manager to catch the expected exception.
    3. Assert that the error message contains "Cannot divide by zero.".

    Examples:
    >>> test_division_by_zero(1, 0)
    >>> test_division_by_zero(-1, 0)
    """
    
    # Use pytest's context manager to check for a ValueError when dividing by zero
    with pytest.raises(ValueError, match="Cannot divide by zero.") as excinfo:
        # Attempt to divide 'a' by 'b', which should raise a ValueError
        Operations.division(a, b)
    
    # Assert that the exception message contains the expected error message
    assert "Cannot divide by zero." in str(excinfo.value), \
        f"Expected error message 'Cannot divide by zero.', but got '{excinfo.value}'"

