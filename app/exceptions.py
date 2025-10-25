# Exception Hierarchy

class CalculatorError(Exception):
    """
    Base exception for all calculator-specific errors.

    This is the parent class for all our custom exceptions. By having a common
    base class, we can catch "any calculator error" with a single except clause
    if we want to, or catch specific types individually.
    """
    pass


class ValidationError(CalculatorError):
    """
    Raised when user input doesn't pass validation checks.

    This exception happens when someone enters something invalid - like typing
    letters instead of numbers, entering a number that's too large, or providing
    input in the wrong format. It's our way of saying "hold on, that input
    doesn't look right."
    """
    pass


class OperationError(CalculatorError):
    """
    Raised when something goes wrong during a calculation.

    This exception covers problems that happen while actually doing math - things
    like dividing by zero, trying to take the square root of a negative number,
    or using an operation that doesn't exist.
    """
    pass


class ConfigurationError(CalculatorError):
    """
    Raised when the calculator's settings are invalid.

    This exception happens when there's a problem with how the calculator is
    configured - like an invalid file path, a negative history size, or a
    missing required setting.
    """
    pass