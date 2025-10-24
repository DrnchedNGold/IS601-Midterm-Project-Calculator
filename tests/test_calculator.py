""" tests/test_calculator.py """
import sys
from io import StringIO
from app.calculator import calculator


# Helper function to capture print statements
def run_calculator_with_input(monkeypatch, inputs):
    """
    Simulates user input and captures output from the calculator REPL.
    
    :param monkeypatch: pytest fixture to simulate user input
    :param inputs: list of inputs to simulate
    :return: captured output as a string
    """
    input_iterator = iter(inputs)
    monkeypatch.setattr('builtins.input', lambda _: next(input_iterator))

    # Capture the output of the calculator
    captured_output = StringIO()
    sys.stdout = captured_output
    calculator()
    sys.stdout = sys.__stdout__  # Reset stdout
    return captured_output.getvalue()


# Positive Tests
def test_addition(monkeypatch):
    """Test addition operation in REPL."""
    inputs = ["add 7 8", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Result: 15.0" in output


def test_subtraction(monkeypatch):
    """Test subtraction operation in REPL."""
    inputs = ["subtract 1 0", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Result: 1.0" in output


def test_multiplication(monkeypatch):
    """Test multiplication operation in REPL."""
    inputs = ["multiply 9 4", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Result: 36.0" in output


def test_division(monkeypatch):
    """Test division operation in REPL."""
    inputs = ["divide 18 4", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Result: 4.5" in output


# Negative Tests
def test_invalid_operation(monkeypatch):
    """Test invalid operation in REPL."""
    inputs = ["modulus 8 3", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Unknown operation" in output


def test_invalid_input_format(monkeypatch):
    """Test invalid input format in REPL."""
    inputs = ["add five three", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Invalid input. Please follow the format" in output


def test_division_by_zero(monkeypatch):
    """Test division by zero in REPL."""
    inputs = ["divide 3 0", "exit"]
    output = run_calculator_with_input(monkeypatch, inputs)
    assert "Cannot divide by zero" in output