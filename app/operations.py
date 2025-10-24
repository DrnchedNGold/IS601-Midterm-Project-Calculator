"""
app/operations.py
Basic arithmetic operations
"""

def addition(a: float, b: float) -> float:
    """Add two float numbers"""
    return a + b


def subtraction(a: float, b: float) -> float:
    """Subtract two float numbers"""
    return a - b

def multiplication(a: float, b: float) -> float:
    """Multiply two float numbers"""
    return a * b

def division(a: float, b: float) -> float:
    """Divide two float numbers"""
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b