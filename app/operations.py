# Operation Classes

from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Dict
from app.exceptions import ValidationError


class Operation(ABC):
    """
    Abstract base class that defines what all operations need to implement.

    Think of it like having different attachments for a power drill - they all
    fit the same way, but each does something different.
    """

    @abstractmethod
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Performs the actual calculation.

        Every operation must implement this method. It takes two numbers and
        returns the result of applying the operation to them.

        Args:
            a: First number
            b: Second number

        Returns:
            Decimal: Result of the operation

        Raises:
            OperationError: If something goes wrong during calculation
        """
        pass  # pragma: no cover

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        """
        Checks if the operands are valid for this operation.

        The base implementation does nothing, but specific operations can override
        this to add their own validation rules. For example, Division checks that
        we're not dividing by zero.

        This is like a pre-flight check before doing the actual calculation.

        Args:
            a: First number to validate
            b: Second number to validate

        Raises:
            ValidationError: If the operands aren't valid for this operation
        """
        pass

    def __str__(self) -> str:
        """
        Returns a readable name for this operation.

        This is what gets displayed when we show the operation to users or in logs.
        By default, it just uses the class name (like "Addition" or "Division").

        Returns:
            str: Name of the operation
        """
        return self.__class__.__name__


class Addition(Operation):
    """
    Implements addition of two numbers.

    Simple and straightforward - just adds the two operands together.
    """

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Adds two numbers together.

        Args:
            a: First number
            b: Second number

        Returns:
            Decimal: Sum of a and b
        """
        self.validate_operands(a, b)
        return a + b


class Subtraction(Operation):
    """
    Implements subtraction of one number from another.

    Takes the first number and subtracts the second from it.
    """

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Subtracts b from a.

        Args:
            a: Number to subtract from
            b: Number to subtract

        Returns:
            Decimal: Difference (a - b)
        """
        self.validate_operands(a, b)
        return a - b


class Multiplication(Operation):
    """
    Implements multiplication of two numbers.

    Multiplies the two operands together.
    """

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Multiplies two numbers.

        Args:
            a: First number
            b: Second number

        Returns:
            Decimal: Product of a and b
        """
        self.validate_operands(a, b)
        return a * b


class Division(Operation):
    """
    Implements division of one number by another.

    This operation needs special validation because dividing by zero is
    mathematically undefined and would crash the program.
    """

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        """
        Checks that we're not trying to divide by zero.

        This overrides the base validation to add a division-specific check.
        We call the parent's validate_operands first (in case it does something
        in the future), then add our own check.

        Args:
            a: Number being divided (dividend)
            b: Number dividing by (divisor)

        Raises:
            ValidationError: If b is zero
        """
        super().validate_operands(a, b)
        if b == 0:
            raise ValidationError("Division by zero is not allowed")

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Divides a by b.

        Args:
            a: Dividend (number being divided)
            b: Divisor (number dividing by)

        Returns:
            Decimal: Quotient (a / b)
        """
        self.validate_operands(a, b)
        return a / b


class Power(Operation):
    """
    Implements exponentiation (raising a number to a power).

    Calculates a^b (a to the power of b). We don't support negative exponents
    because they result in fractions that might not be what users expect.
    """

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        """
        Checks that the exponent isn't negative.

        Negative exponents would give fractional results (like 2^-3 = 0.125),
        which we've decided not to support to keep things simpler.

        Args:
            a: Base number
            b: Exponent

        Raises:
            ValidationError: If the exponent is negative
        """
        super().validate_operands(a, b)
        if b < 0:
            raise ValidationError("Negative exponents not supported")

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Calculates a raised to the power of b.

        We convert to float for the calculation (Python's pow function works
        with floats), then convert back to Decimal for precision.

        Args:
            a: Base number
            b: Exponent

        Returns:
            Decimal: Result of a^b
        """
        self.validate_operands(a, b)
        return Decimal(pow(float(a), float(b)))


class Root(Operation):
    """
    Implements root calculation (like square root, cube root, etc.).

    Calculates the bth root of a. For example, if b=2, this is square root,
    if b=3, this is cube root, and so on.
    """

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        """
        Checks that root calculation is mathematically valid.

        We can't take the root of a negative number (at least not with real
        numbers), and we can't use zero as the root degree (that's undefined).

        Args:
            a: Number to take the root of
            b: Degree of the root (2 for square root, 3 for cube root, etc.)

        Raises:
            ValidationError: If a is negative or b is zero
        """
        super().validate_operands(a, b)
        if a < 0:
            raise ValidationError("Cannot calculate root of negative number")
        if b == 0:
            raise ValidationError("Zero root is undefined")

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Calculates the bth root of a.

        This uses the mathematical relationship: the bth root of a is the same
        as a^(1/b). We convert to float for the calculation, then back to Decimal.

        Args:
            a: Number to take the root of
            b: Degree of the root

        Returns:
            Decimal: The bth root of a
        """
        self.validate_operands(a, b)
        return Decimal(pow(float(a), 1 / float(b)))


class OperationFactory:
    """
    Factory that creates the right operation based on what the user asks for.

    This implements the Factory pattern - instead of having the calculator
    create operations directly (which would require a bunch of if statements),
    we have this factory do it. The calculator just says "give me an add
    operation" and the factory figures out which class to instantiate.

    This makes it easy to add new operations - just register them with the
    factory and everything else works automatically.
    """

    # Dictionary mapping operation names to their classes
    # This is like a menu - when someone orders "add", we know to give them Addition
    _operations: Dict[str, type] = {
        'add': Addition,
        'subtract': Subtraction,
        'multiply': Multiplication,
        'divide': Division,
        'power': Power,
        'root': Root
    }

    @classmethod
    def register_operation(cls, name: str, operation_class: type) -> None:
        """
        Adds a new operation type to the factory.

        This lets us extend the calculator with new operations without modifying
        this file. Just create a new Operation subclass and register it here.

        Args:
            name: What users will type to use this operation (like 'modulus')
            operation_class: The class that implements the operation

        Raises:
            TypeError: If the class doesn't inherit from Operation
        """
        # Make sure the new operation follows the rules (inherits from Operation)
        if not issubclass(operation_class, Operation):
            raise TypeError("Operation class must inherit from Operation")
        cls._operations[name.lower()] = operation_class

    @classmethod
    def create_operation(cls, operation_type: str) -> Operation:
        """
        Creates and returns an instance of the requested operation.

        This is the main factory method. Give it an operation name (like 'add')
        and it gives you back an operation object ready to use.

        Args:
            operation_type: Name of the operation to create

        Returns:
            Operation: A new instance of the requested operation

        Raises:
            ValueError: If the operation type isn't recognized
        """
        # Look up the operation class in our dictionary (case-insensitive)
        operation_class = cls._operations.get(operation_type.lower())
        if not operation_class:
            raise ValueError(f"Unknown operation: {operation_type}")
        # Create and return a new instance of that class
        return operation_class()