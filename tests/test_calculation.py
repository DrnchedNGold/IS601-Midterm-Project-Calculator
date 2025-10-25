# Author: Varun Sabbineni 10/6/2025

"""
Tests for the Calculation model class.
"""

import pytest
from decimal import Decimal
from datetime import datetime
from app.calculation import Calculation
from app.exceptions import OperationError
import logging


def test_addition():
    """Test that addition calculates correctly."""
    calc = Calculation(operation="Addition", operand1=Decimal("2"), operand2=Decimal("3"))
    assert calc.result == Decimal("5")


def test_subtraction():
    """Test that subtraction calculates correctly."""
    calc = Calculation(operation="Subtraction", operand1=Decimal("5"), operand2=Decimal("3"))
    assert calc.result == Decimal("2")


def test_multiplication():
    """Test that multiplication calculates correctly."""
    calc = Calculation(operation="Multiplication", operand1=Decimal("4"), operand2=Decimal("2"))
    assert calc.result == Decimal("8")


def test_division():
    """Test that division calculates correctly."""
    calc = Calculation(operation="Division", operand1=Decimal("8"), operand2=Decimal("2"))
    assert calc.result == Decimal("4")


def test_division_by_zero():
    """Test that dividing by zero raises the correct error."""
    with pytest.raises(OperationError, match="Division by zero is not allowed"):
        Calculation(operation="Division", operand1=Decimal("8"), operand2=Decimal("0"))


def test_power():
    """Test that exponentiation calculates correctly."""
    calc = Calculation(operation="Power", operand1=Decimal("2"), operand2=Decimal("3"))
    assert calc.result == Decimal("8")


def test_negative_power():
    """Test that negative exponents are rejected."""
    with pytest.raises(OperationError, match="Negative exponents are not supported"):
        Calculation(operation="Power", operand1=Decimal("2"), operand2=Decimal("-3"))


def test_root():
    """Test that root calculation works correctly."""
    calc = Calculation(operation="Root", operand1=Decimal("16"), operand2=Decimal("2"))
    assert calc.result == Decimal("4")


def test_invalid_root():
    """Test that root of negative number is rejected."""
    with pytest.raises(OperationError, match="Cannot calculate root of negative number"):
        Calculation(operation="Root", operand1=Decimal("-16"), operand2=Decimal("2"))


def test_unknown_operation():
    """Test that unknown operations raise an error."""
    with pytest.raises(OperationError, match="Unknown operation"):
        Calculation(operation="Unknown", operand1=Decimal("5"), operand2=Decimal("3"))


def test_to_dict():
    """Test that calculations can be converted to dictionaries."""
    calc = Calculation(operation="Addition", operand1=Decimal("2"), operand2=Decimal("3"))
    result_dict = calc.to_dict()
    assert result_dict == {
        "operation": "Addition",
        "operand1": "2",
        "operand2": "3",
        "result": "5",
        "timestamp": calc.timestamp.isoformat()
    }


def test_from_dict():
    """Test that calculations can be created from dictionaries."""
    data = {
        "operation": "Addition",
        "operand1": "2",
        "operand2": "3",
        "result": "5",
        "timestamp": datetime.now().isoformat()
    }
    calc = Calculation.from_dict(data)
    assert calc.operation == "Addition"
    assert calc.operand1 == Decimal("2")
    assert calc.operand2 == Decimal("3")
    assert calc.result == Decimal("5")


def test_invalid_from_dict():
    """Test that invalid dictionary data raises an error."""
    data = {
        "operation": "Addition",
        "operand1": "invalid",
        "operand2": "3",
        "result": "5",
        "timestamp": datetime.now().isoformat()
    }
    with pytest.raises(OperationError, match="Invalid calculation data"):
        Calculation.from_dict(data)


def test_format_result():
    """Test that results can be formatted with different precision levels."""
    calc = Calculation(operation="Division", operand1=Decimal("1"), operand2=Decimal("3"))
    assert calc.format_result(precision=2) == "0.33"
    assert calc.format_result(precision=10) == "0.3333333333"


def test_equality():
    """Test that calculations can be compared for equality."""
    calc1 = Calculation(operation="Addition", operand1=Decimal("2"), operand2=Decimal("3"))
    calc2 = Calculation(operation="Addition", operand1=Decimal("2"), operand2=Decimal("3"))
    calc3 = Calculation(operation="Subtraction", operand1=Decimal("5"), operand2=Decimal("3"))
    assert calc1 == calc2
    assert calc1 != calc3


def test_from_dict_result_mismatch(caplog):
    """Test that loading a calculation with mismatched result logs a warning."""
    # Create data with an incorrect result
    data = {
        "operation": "Addition",
        "operand1": "2",
        "operand2": "3",
        "result": "10",  # Wrong result to trigger warning
        "timestamp": datetime.now().isoformat()
    }

    # Load the calculation and capture log output
    with caplog.at_level(logging.WARNING):
        calc = Calculation.from_dict(data)

    # Verify the warning was logged
    assert "Loaded calculation result 10 differs from computed result 5" in caplog.text

def test_str_representation():
    """Test the __str__ method of Calculation."""
    calc = Calculation(operation="Addition", operand1=Decimal("2"), operand2=Decimal("3"))
    assert str(calc) == "Addition(2, 3) = 5"

def test_repr_representation():
    """Test the __repr__ method of Calculation."""
    calc = Calculation(operation="Addition", operand1=Decimal("2"), operand2=Decimal("3"))
    rep = repr(calc)
    assert "Calculation(operation='Addition'" in rep
    assert "operand1=2" in rep
    assert "operand2=3" in rep
    assert "result=5" in rep

def test_zero_root_error():
    """Test that root with degree zero raises the correct error."""
    with pytest.raises(OperationError, match="Zero root is undefined"):
        Calculation(operation="Root", operand1=Decimal("16"), operand2=Decimal("0"))

def test_calculation_invalid_operand():
    """Test calculation error handling for invalid operand types."""
    with pytest.raises(OperationError):
        Calculation(operation="Addition", operand1="not_a_number", operand2=Decimal("2"))

def test_format_result_fallback():
    """Test format_result fallback when InvalidOperation occurs."""
    calc = Calculation(operation="Addition", operand1=Decimal("2"), operand2=Decimal("3"))
    # Monkeypatch result to a value that will cause quantize to fail
    calc.result = Decimal("NaN")
    # Should fallback to str(self.result)
    assert calc.format_result() == "NaN"
