# tests/test_operations.py

"""
Tests for operation classes and the OperationFactory.
"""

import pytest
from decimal import Decimal
from typing import Any, Dict, Type

from app.exceptions import ValidationError
from app.operations import (
    Operation,
    Addition,
    Subtraction,
    Multiplication,
    Division,
    Power,
    Root,
    Modulus,
    IntegerDivision,
    PercentageCalculation,
    AbsoluteDifference,
    OperationFactory,
)

class TestOperation:
    """Tests for the base Operation class."""

    def test_str_representation(self):
        """Test that operations display their class name."""
        class TestOp(Operation):
            def execute(self, a: Decimal, b: Decimal) -> Decimal:
                return a

        assert str(TestOp()) == "TestOp"


class BaseOperationTest:
    """
    Base test class for testing operations.
    """

    operation_class: Type[Operation]
    valid_test_cases: Dict[str, Dict[str, Any]]
    invalid_test_cases: Dict[str, Dict[str, Any]]

    def test_valid_operations(self):
        """Test operation with valid inputs."""
        operation = self.operation_class()
        for name, case in self.valid_test_cases.items():
            a = Decimal(str(case["a"]))
            b = Decimal(str(case["b"]))
            expected = Decimal(str(case["expected"]))
            result = operation.execute(a, b)
            assert result == expected, f"Failed case: {name}"

    def test_invalid_operations(self):
        """Test that invalid inputs raise appropriate errors."""
        operation = self.operation_class()
        for name, case in self.invalid_test_cases.items():
            a = Decimal(str(case["a"]))
            b = Decimal(str(case["b"]))
            error = case.get("error", ValidationError)
            error_message = case.get("message", "")

            with pytest.raises(error, match=error_message):
                operation.execute(a, b)


class TestAddition(BaseOperationTest):
    """Tests for addition operation."""

    operation_class = Addition
    valid_test_cases = {
        "positive_numbers": {"a": "5", "b": "3", "expected": "8"},
        "negative_numbers": {"a": "-5", "b": "-3", "expected": "-8"},
        "mixed_signs": {"a": "-5", "b": "3", "expected": "-2"},
        "zero_sum": {"a": "5", "b": "-5", "expected": "0"},
        "decimals": {"a": "5.5", "b": "3.3", "expected": "8.8"},
        "large_numbers": {"a": "1e10", "b": "1e10", "expected": "20000000000"},
    }
    invalid_test_cases = {}  # Addition accepts all inputs


class TestSubtraction(BaseOperationTest):
    """Tests for subtraction operation."""

    operation_class = Subtraction
    valid_test_cases = {
        "positive_numbers": {"a": "5", "b": "3", "expected": "2"},
        "negative_numbers": {"a": "-5", "b": "-3", "expected": "-2"},
        "mixed_signs": {"a": "-5", "b": "3", "expected": "-8"},
        "zero_result": {"a": "5", "b": "5", "expected": "0"},
        "decimals": {"a": "5.5", "b": "3.3", "expected": "2.2"},
        "large_numbers": {"a": "1e10", "b": "1e9", "expected": "9000000000"},
    }
    invalid_test_cases = {}  # Subtraction accepts all inputs


class TestMultiplication(BaseOperationTest):
    """Tests for multiplication operation."""

    operation_class = Multiplication
    valid_test_cases = {
        "positive_numbers": {"a": "5", "b": "3", "expected": "15"},
        "negative_numbers": {"a": "-5", "b": "-3", "expected": "15"},
        "mixed_signs": {"a": "-5", "b": "3", "expected": "-15"},
        "multiply_by_zero": {"a": "5", "b": "0", "expected": "0"},
        "decimals": {"a": "5.5", "b": "3.3", "expected": "18.15"},
        "large_numbers": {"a": "1e5", "b": "1e5", "expected": "10000000000"},
    }
    invalid_test_cases = {}  # Multiplication accepts all inputs


class TestDivision(BaseOperationTest):
    """Tests for division operation."""

    operation_class = Division
    valid_test_cases = {
        "positive_numbers": {"a": "6", "b": "2", "expected": "3"},
        "negative_numbers": {"a": "-6", "b": "-2", "expected": "3"},
        "mixed_signs": {"a": "-6", "b": "2", "expected": "-3"},
        "decimals": {"a": "5.5", "b": "2", "expected": "2.75"},
        "divide_zero": {"a": "0", "b": "5", "expected": "0"},
    }
    invalid_test_cases = {
        "divide_by_zero": {
            "a": "5",
            "b": "0",
            "error": ValidationError,
            "message": "Division by zero is not allowed"
        },
    }


class TestPower(BaseOperationTest):
    """Tests for power (exponentiation) operation."""

    operation_class = Power
    valid_test_cases = {
        "positive_base_and_exponent": {"a": "2", "b": "3", "expected": "8"},
        "zero_exponent": {"a": "5", "b": "0", "expected": "1"},
        "one_exponent": {"a": "5", "b": "1", "expected": "5"},
        "decimal_base": {"a": "2.5", "b": "2", "expected": "6.25"},
        "zero_base": {"a": "0", "b": "5", "expected": "0"},
    }
    invalid_test_cases = {
        "negative_exponent": {
            "a": "2",
            "b": "-3",
            "error": ValidationError,
            "message": "Negative exponents not supported"
        },
    }


class TestRoot(BaseOperationTest):
    """Tests for root operation."""

    operation_class = Root
    valid_test_cases = {
        "square_root": {"a": "9", "b": "2", "expected": "3"},
        "cube_root": {"a": "27", "b": "3", "expected": "3"},
        "fourth_root": {"a": "16", "b": "4", "expected": "2"},
        "decimal_root": {"a": "2.25", "b": "2", "expected": "1.5"},
    }
    invalid_test_cases = {
        "negative_base": {
            "a": "-9",
            "b": "2",
            "error": ValidationError,
            "message": "Cannot calculate root of negative number"
        },
        "zero_root": {
            "a": "9",
            "b": "0",
            "error": ValidationError,
            "message": "Zero root is undefined"
        },
    }


class TestModulus(BaseOperationTest):
    """Tests for modulus operation."""

    operation_class = Modulus
    valid_test_cases = {
        "positive_numbers": {"a": "10", "b": "3", "expected": "1"},
        "even_division": {"a": "8", "b": "4", "expected": "0"},
        "larger_modulus": {"a": "5", "b": "7", "expected": "5"},
        "decimal_modulus": {"a": "10.5", "b": "3", "expected": "1.5"},
        "negative_dividend": {"a": "-10", "b": "3", "expected": "-1"},
        "negative_divisor": {"a": "10", "b": "-3", "expected": "1"},
    }
    invalid_test_cases = {
        "modulus_by_zero": {
            "a": "10",
            "b": "0",
            "error": ValidationError,
            "message": "Modulus by zero is not allowed"
        },
    }

class TestIntegerDivision(BaseOperationTest):
    """Tests for integer division operation."""

    operation_class = IntegerDivision
    valid_test_cases = {
        "positive_numbers": {"a": "10", "b": "3", "expected": "3"},
        "even_division": {"a": "8", "b": "4", "expected": "2"},
        "decimal_result": {"a": "7", "b": "2", "expected": "3"},
        "decimal_operands": {"a": "10.8", "b": "3", "expected": "3"},
        "negative_dividend": {"a": "-10", "b": "3", "expected": "-3"},
        "negative_divisor": {"a": "10", "b": "-3", "expected": "-3"},
        "both_negative": {"a": "-10", "b": "-3", "expected": "3"},
    }
    invalid_test_cases = {
        "divide_by_zero": {
            "a": "10",
            "b": "0",
            "error": ValidationError,
            "message": "Integer division by zero is not allowed"
        },
    }

class TestPercentageCalculation(BaseOperationTest):
    """Tests for percentage calculation operation."""

    operation_class = PercentageCalculation
    valid_test_cases = {
        "basic_percentage": {"a": "25", "b": "100", "expected": "25"},
        "greater_than_100": {"a": "150", "b": "100", "expected": "150"},
        "decimal_percentage": {"a": "33", "b": "100", "expected": "33"},
        "small_percentage": {"a": "1", "b": "8", "expected": "12.5"},
        "zero_numerator": {"a": "0", "b": "100", "expected": "0"},
        "fractional_result": {"a": "1", "b": "3", "expected": "33.33333333333333333333333333"},
    }
    invalid_test_cases = {
        "zero_denominator": {
            "a": "25",
            "b": "0",
            "error": ValidationError,
            "message": "Cannot calculate percentage with zero base"
        },
    }

class TestAbsoluteDifference(BaseOperationTest):
    """Tests for absolute difference operation."""

    operation_class = AbsoluteDifference
    valid_test_cases = {
        "positive_difference": {"a": "10", "b": "3", "expected": "7"},
        "negative_difference": {"a": "3", "b": "10", "expected": "7"},
        "zero_difference": {"a": "5", "b": "5", "expected": "0"},
        "decimal_difference": {"a": "5.5", "b": "2.2", "expected": "3.3"},
        "negative_numbers": {"a": "-5", "b": "-3", "expected": "2"},
        "mixed_signs": {"a": "-5", "b": "3", "expected": "8"},
        "large_numbers": {"a": "1000000", "b": "999999", "expected": "1"},
    }
    invalid_test_cases = {}  # Absolute difference accepts all inputs

class TestOperationFactory:
    """Tests for the OperationFactory."""

    def test_create_valid_operations(self):
        """Test creating all valid operations."""
        operation_map = {
            'add': Addition,
            'subtract': Subtraction,
            'multiply': Multiplication,
            'divide': Division,
            'power': Power,
            'root': Root,
            'modulus': Modulus,
            'int_divide': IntegerDivision,
            'percent': PercentageCalculation,
            'abs_diff': AbsoluteDifference,
        }

        for op_name, op_class in operation_map.items():
            operation = OperationFactory.create_operation(op_name)
            assert isinstance(operation, op_class)
            
            # Test case-insensitive operation names
            operation = OperationFactory.create_operation(op_name.upper())
            assert isinstance(operation, op_class)

    def test_create_invalid_operation(self):
        """Test that requesting unknown operation raises error."""
        with pytest.raises(ValueError, match="Unknown operation: invalid_op"):
            OperationFactory.create_operation("invalid_op")

    def test_register_valid_operation(self):
        """Test registering a new operation with the factory."""
        class NewOperation(Operation):
            def execute(self, a: Decimal, b: Decimal) -> Decimal:
                return a

        OperationFactory.register_operation("new_op", NewOperation)
        operation = OperationFactory.create_operation("new_op")
        assert isinstance(operation, NewOperation)

    def test_register_invalid_operation(self):
        """Test that registering non-Operation class raises error."""
        class InvalidOperation:
            pass

        with pytest.raises(TypeError, match="Operation class must inherit"):
            OperationFactory.register_operation("invalid", InvalidOperation)
