""" 
tests/test_operations.py 
"""

import pytest
from app.operations import Operations

# ========================================
# Tests for 'addition' Method
# ========================================

def test_addition_positive():
    """
    Test 'addition' method with two positive numbers.
    """
    # Arrange
    a = 10.0
    b = 5.0
    expected_result = 15.0

    # Act
    result = Operations.addition(a, b)

    # Assert
    assert result == expected_result, f"Expected {a} + {b} to be {expected_result}, got {result}"

def test_addition_negative_numbers():
    """
    Test 'addition' method with two negative numbers.
    """
    # Arrange
    a = -10.0
    b = -5.0
    expected_result = -15.0

    # Act
    result = Operations.addition(a, b)

    # Assert
    assert result == expected_result, f"Expected {a} + {b} to be {expected_result}, got {result}"

def test_addition_positive_negative():
    """
    Test 'addition' method with one positive and one negative number.
    """
    # Arrange
    a = 10.0
    b = -5.0
    expected_result = 5.0

    # Act
    result = Operations.addition(a, b)

    # Assert
    assert result == expected_result, f"Expected {a} + ({b}) to be {expected_result}, got {result}"

def test_addition_with_zero():
    """
    Test 'addition' method with zero as one of the operands.
    """
    # Arrange
    a = 10.0
    b = 0.0
    expected_result = 10.0

    # Act
    result = Operations.addition(a, b)

    # Assert
    assert result == expected_result, f"Expected {a} + {b} to be {expected_result}, got {result}"

# ========================================
# Tests for 'subtraction' Method
# ========================================

def test_subtraction_positive():
    """
    Test 'subtraction' method with two positive numbers.
    """
    # Arrange
    a = 10.0
    b = 5.0
    expected_result = 5.0

    # Act
    result = Operations.subtraction(a, b)

    # Assert
    assert result == expected_result, f"Expected {a} - {b} to be {expected_result}, got {result}"

def test_subtraction_negative_numbers():
    """
    Test the 'subtraction' method with two negative numbers.
    """
    # Arrange
    a = -10.0
    b = -5.0
    expected_result = -5.0

    # Act
    result = Operations.subtraction(a, b)

    # Assert
    assert result == expected_result, f"Expected {a} - ({b}) to be {expected_result}, got {result}"

def test_subtraction_positive_negative():
    """
    Test the 'subtraction' method with one positive and one negative number.
    """
    # Arrange
    a = 10.0
    b = -5.0
    expected_result = 15.0

    # Act
    result = Operations.subtraction(a, b)

    # Assert
    assert result == expected_result, f"Expected {a} - ({b}) to be {expected_result}, got {result}"

def test_subtraction_with_zero():
    """
    Test the 'subtraction' method with zero as one of the operands.
    """
    # Arrange
    a = 10.0
    b = 0.0
    expected_result = 10.0

    # Act
    result = Operations.subtraction(a, b)

    # Assert
    assert result == expected_result, f"Expected {a} - {b} to be {expected_result}, got {result}"

# ========================================
# Tests for 'multiplication' Method
# ========================================

def test_multiplication_positive():
    """
    Test 'multiplication' method with two positive numbers.
    """
    # Arrange
    a = 10.0
    b = 5.0
    expected_result = 50.0

    # Act
    result = Operations.multiplication(a, b)

    # Assert
    assert result == expected_result, f"Expected {a} * {b} to be {expected_result}, got {result}"

def test_multiplication_negative_numbers():
    """
    Test the 'multiplication' method with two negative numbers.
    """
    # Arrange
    a = -10.0
    b = -5.0
    expected_result = 50.0

    # Act
    result = Operations.multiplication(a, b)

    # Assert
    assert result == expected_result, f"Expected {a} * {b} to be {expected_result}, got {result}"

def test_multiplication_positive_negative():
    """
    Test the 'multiplication' method with one positive and one negative number.
    """
    # Arrange
    a = 10.0
    b = -5.0
    expected_result = -50.0

    # Act
    result = Operations.multiplication(a, b)

    # Assert
    assert result == expected_result, f"Expected {a} * ({b}) to be {expected_result}, got {result}"

def test_multiplication_with_zero():
    """
    Test the 'multiplication' method with zero as one of the operands.
    """
    # Arrange
    a = 10.0
    b = 0.0
    expected_result = 0.0

    # Act
    result = Operations.multiplication(a, b)

    # Assert
    assert result == expected_result, f"Expected {a} * {b} to be {expected_result}, got {result}"

# ========================================
# Tests for 'division' Method
# ========================================

def test_division():
    """
    Test 'division' method with two positive numbers.
    """
    # Arrange
    a = 10.0
    b = 5.0
    expected_result = 2.0

    # Act
    result = Operations.division(a, b)

    # Assert
    assert result == expected_result, f"Expected {a} / {b} to be {expected_result}, got {result}"

def test_division_negative_numbers():
    """
    Test the 'division' method with two negative numbers.
    """
    # Arrange
    a = -10.0
    b = -5.0
    expected_result = 2.0

    # Act
    result = Operations.division(a, b)

    # Assert
    assert result == expected_result, f"Expected {a} / {b} to be {expected_result}, got {result}"

def test_division_positive_negative():
    """
    Test the 'division' method with one positive and one negative number.
    """
    # Arrange
    a = 10.0
    b = -5.0
    expected_result = -2.0

    # Act
    result = Operations.division(a, b)

    # Assert
    assert result == expected_result, f"Expected {a} / ({b}) to be {expected_result}, got {result}"

def test_division_with_zero_divisor():
    """
    Test the 'division' method with zero as the divisor.
    """
    # Arrange
    a = 10.0
    b = 0.0

    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        Operations.division(a, b)
    
    # Verify that the exception message is as expected
    assert str(exc_info.value) == "Cannot divide by zero."

def test_division_with_zero_numerator():
    """
    Test the 'division' method with zero as the numerator.
    """
    # Arrange
    a = 0.0
    b = 5.0
    expected_result = 0.0

    # Act
    result = Operations.division(a, b)

    # Assert
    assert result == expected_result, f"Expected {a} / {b} to be {expected_result}, got {result}"

# ===================================================
# Negative Test Case: Invalid Inputs
# ===================================================

@pytest.mark.parametrize("calc_method, a, b, expected_exception", [
    (Operations.addition, '10', 5.0, TypeError),
    (Operations.subtraction, 10.0, '5', TypeError),
    (Operations.multiplication, '10', '5', TypeError),
    (Operations.division, 10.0, '5', TypeError),
])
def test_operations_invalid_input_types(calc_method, a, b, expected_exception):
    """
    Test that arithmetic methods raise TypeError when provided with invalid input types.
    
    This test verifies that providing non-float inputs to the arithmetic methods raises
    a TypeError, as the operations are intended for floating-point numbers.
    """
    # Arrange
    # No setup needed as the invalid inputs are provided directly

    # Act & Assert
    with pytest.raises(expected_exception):
        calc_method(a, b)
