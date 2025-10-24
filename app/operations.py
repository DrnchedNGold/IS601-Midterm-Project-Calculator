"""
app/operations.py
"""

class Operations:
    """
    Operations class for basic arithmetic operations (addition, subtraction, multiplication, division)
    Using static methods to perform operations without instantiating the class.
    """

    @staticmethod
    def addition(a: float, b: float) -> float:
        """
        This static method takes two floating point numbers (a and b) and returns their sum (a + b).
        Float means 'a', 'b', and the result should be numbers with decimal points.
        Example: if we call Operations.addition(5.0, 3.0), it will return 8.0.
        """
        return a + b

    @staticmethod
    def subtraction(a: float, b: float) -> float:
        """
        This static method takes two floating point numbers (a and b) and returns their difference (a - b).
        Float means 'a', 'b', and the result should be numbers with decimal points.
        Example: if we call Operations.subtraction(10.0, 4.0), it will return 6.0.
        """
        return a - b
    @staticmethod
    def multiplication(a: float, b: float) -> float:
        """
        This static method takes two floating point numbers (a and b) and returns their product (a * b).
        Float means 'a', 'b', and the result should be numbers with decimal points.
        Example: if we call Operations.multiplication(2.0, 3.0), it will return 6.0.
        """
        return a * b

    @staticmethod
    def division(a: float, b: float) -> float:
        """
        This static method takes two numbers (a and b) and returns their quotient (a / b).
        Float means 'a', 'b', and the result should be numbers with decimal points.
        IMPORTANT: before dividing, check that 'b' is not zero because dividing by zero doesn't work. If we try to divide by zero, we get a big error!
        
        If 'b' is zero, we raise a 'ValueError', which is a way of telling the program, "Stop! You can't do this."
        Example: if we call Operations.division(10.0, 2.0), it will return 5.0.
        But if we call Operations.division(10.0, 0.0), it will raise a ValueError and say "Cannot divide by zero."
        """
        if b == 0:
            raise ValueError("Cannot divide by zero.")
        return a / b