# calculator_calculations.py

# Abstract Base Classes (ABCs) allow us to define a contract for our subclasses, specifying 
# methods that they must implement. This helps in establishing a standard interface for 
# similar objects without enforcing specific details on how they should work.
from abc import ABC, abstractmethod
from app.operations import Operations

# ========================================
# Abstract Base Class: Calculation
# ========================================
class Calculation(ABC):
    """
    ABC that defines blueprint and establishes a consistent interface for all calculations in the program.
    Each calculation must implement the 'perform' method.
    """

    def __init__(self, a: float, b: float) -> None:
        """
        Initializes a Calculation instance with two operands (numbers involved in the calculation).

        **Parameters:**
        - `a (float)`: The first operand.
        - `b (float)`: The second operand.
        """
        self.a: float = a
        self.b: float = b

    @abstractmethod
    def execute(self) -> float:
        """
        Perform the calculation using the specified operation.
        Must be implemented by subclasses.

        **Returns:**
        - `float`: The result of the calculation.
        """
        pass    # The actual implementation will be provided by the subclass.

    def __str__(self) -> str:
        """
        User-friendly string representation of Calculation instance, showing the operation name, operands, and result.
        
        **Returns:**
        - `str`: A string describing the calculation and its result.
        """
        result = self.execute()     # run the calculation and store in result
        operation_name = self.__class__.__name__.replace('Calculation', '')     # get operaiton name
        return f"{self.__class__.__name__}: {self.a} {operation_name} {self.b} = {result}"
    
    def __repr__(self) -> str:
        """
        Provides a detailed string representation of the Calculation instance for debugging,showing the class name and operand values.
        
        **Returns:**
        - `str`: A string containing the class name and operands.
        """
        return f"{self.__class__.__name__} (a={self.a}, b={self.b})"

# ========================================
# Factory Class: CalculationFactory
# ========================================
class CalculationFactory:
    """
    Factory class to create Calculation instances based on the specified operation.
    """

    _calculations = {}

    @classmethod
    def register_calculation(cls, calculation_type: str):
        """
        Decorator to register a Calculation subclass with a specific operation type.

        **Parameters:**
        - `calculation_type (str)`: The operation type (e.g., 'add', 'subtract').
        - `calculation_cls (type)`: The Calculation subclass to register.
        """
        def decorator(subclass):
            calculation_type_lower = calculation_type.lower()
            if calculation_type_lower in cls._calculations:
                raise ValueError(f"Calculation type '{calculation_type}' is already registered.")
            cls._calculations[calculation_type_lower] = subclass
            return subclass
        return decorator

    @classmethod
    def create_calculation(cls, calculation_type: str, a: float, b: float) -> Calculation:
        """
        Factory method to create and return a Calculation instance based on the operation.

        **Parameters:**
        - `calculation_type (str)`: The operation type ('add', 'subtract', 'multiply', 'divide').
        - `a (float)`: The first operand.
        - `b (float)`: The second operand.

        **Returns:**
        - `Calculation`: An instance of a subclass of Calculation corresponding to the operation.

        **Raises:**
        - `ValueError`: If the operation is not supported.
        """
        calculation_type_lower = calculation_type.lower()
        calculation_class = cls._calculations.get(calculation_type_lower)
        if not calculation_class:
            available_types = ', '.join(cls._calculations.keys())
            raise ValueError(f"Unsupported operation '{calculation_type}'. Supported operations are: {available_types}.")
        return calculation_class(a, b)

# ========================================
# Concrete Calculation Classes
# ========================================
@CalculationFactory.register_calculation('add')
class AddCalculation(Calculation):
    """Concrete Calculation class for addition operation."""
    
    def execute(self) -> float:
        """Perform addition of the two operands."""
        return Operations.addition(self.a, self.b)

@CalculationFactory.register_calculation('subtract')
class SubtractCalculation(Calculation):
    """Concrete Calculation class for subtraction operation."""
    
    def execute(self) -> float:
        """Perform subtraction of the two operands."""
        return Operations.subtraction(self.a, self.b)    

@CalculationFactory.register_calculation('multiply')
class MultiplyCalculation(Calculation):
    """Concrete Calculation class for multiplication operation."""
    
    def execute(self) -> float:
        """Perform multiplication of the two operands."""
        return Operations.multiplication(self.a, self.b)

@CalculationFactory.register_calculation('divide')
class DivideCalculation(Calculation):
    """Concrete Calculation class for division operation."""
    
    def execute(self) -> float:
        """
        Perform division of the two operands.

        **Division by Zero**: Raises ZeroDivisionError if the second operand is zero.
        """
        if self.b == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return Operations.division(self.a, self.b)