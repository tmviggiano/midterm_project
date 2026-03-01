from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Dict
from app.exceptions import ValidationError



class Operation(ABC):
    """
    Abstract base class for calculator
    """


    @abstractmethod
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        pass # pragma: no cover

    def validate_operands(self, a: Decimal, b: Decimal)-> None:
        pass
    def __str__(self):
        return self.__class__.__name__
    


class OperationFactory:

    _operations: Dict[str, type] = {}

    @classmethod
    def register_operations(cls, operation_type: str):
        """Create decorator to assign Operation subclasses as a unique operation"""

        def decorator(subclass):

            operation_type_lower = operation_type.lower()

            if operation_type_lower in cls._operations:
                raise ValueError(f"Operation type '{operation_type}' is already registered")
            
            cls._operations[operation_type_lower] = subclass

            return subclass
        return decorator
    
    @classmethod
    def create_operation(cls, operation_type: str) -> Operation:
        operation_class = cls._operations.get(operation_type.lower())

        if not operation_class:
            raise ValueError(f"Unknown operation: {operation_type}")
        return operation_class()

@OperationFactory.register_operations("add")
class Addition(Operation):

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate_operands(a,b)
        return a + b
    
@OperationFactory.register_operations("subtract")
class Subtraction(Operation):

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate_operands(a,b)
        return a - b
    
@OperationFactory.register_operations("multiply")   
class Multiplication(Operation):

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate_operands(a,b)
        return a * b

@OperationFactory.register_operations("divide")    
class Division(Operation):

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        super().validate_operands(a, b)
        if b == 0:
            raise ValidationError("Division by zero is not allowed")

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate_operands(a,b)
        return a / b

@OperationFactory.register_operations("power")    
class Power(Operation):

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        super().validate_operands(a, b)
        if b < 0:
            raise ValidationError("Negative exponents not supported")

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate_operands(a,b)
        return Decimal((float(a) ** float(b)))
    

@OperationFactory.register_operations("root")
class Root(Operation):

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        super().validate_operands(a, b)

        if a < 0:
            raise ValidationError("Cannot take the root of a negative number")
        if b == 0:
            raise ValidationError("Zeroth root is undefined")
        
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate_operands(a,b)
        return Decimal(float(a) ** (1/float(b)))


@OperationFactory.register_operations("modulus")
class Modulus(Operation):

    def validate_operands(self, a, b):
        super().validate_operands(a, b)

        if b == 0:
            raise ValidationError("Division by zero is not allowed")

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate_operands(a,b)
        return Decimal(float(a) % float(b))
    

@OperationFactory.register_operations("int_division")
class Integer_Division(Operation):

    def validate_operands(self, a: Decimal, b: Decimal) ->None:
        super().validate_operands(a, b)

        if b == 0:
            raise ValidationError("Division by zero is not allowed")
        
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate_operands(a, b)
        return a // b

@OperationFactory.register_operations("abs_diff")
class Absolute_Difference(Operation):

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate_operands(a,b)
        return abs(a-b)
    

