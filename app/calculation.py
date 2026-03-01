from dataclasses import dataclass, field
import datetime
from decimal import Decimal, InvalidOperation
import logging
from typing import Any, Dict
from app.operations import Operation, OperationFactory
from app.exceptions import OperationError

@dataclass
class Calculation:

    result: Decimal = field(init=False)
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)


    def __init__(self, operation_type: str, operand1: Decimal, operand2: Decimal):
        self.operation_type = operation_type
        self.op = OperationFactory.create_operation(operation_type)
        if not self.op:
            raise OperationError(f"Unknowwn operation: {operation_type}")
        self.operand1 = operand1
        self.operand2 = operand2

    
    def __post_init__(self):
        self.result = self.calculate()

    def calculate(self):
        try:
            return self.op(self.operand1, self.operand2)
        except(InvalidOperation, ValueError, ArithmeticError, OperationError) as e:
            raise OperationError(f"Operation failed: {str(e)}")
        
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'operation': self.operation_type,
            'operand1': str(self.operand1),
            'operand2': str(self.operand2),
            'result': str(self.result),
            'timestamp': self.timestamp.isoformat()
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Calculation':
        try:
            calc = Calculation(
                operation_type=data['operation'],
                operand1=Decimal(data['operand1']),
                operand2=Decimal(data['operand2'])
            )

            calc.timestamp = datetime.datetime.fromisoformat(data['timestamp'])

            saved_result = Decimal(data['result'])
            if calc.result != saved_result:
                logging.warning(
                    f"Loaded calculation result {saved_result}"
                    f"differs from computed result {calc.result}"
                ) # pragma: no cover

            return calc
        except (KeyError, InvalidOperation, ValueError) as e:
            raise OperationError(f"Invlaid calculation data: {str(e)}")
        
    def __str__(self) -> str:

        return f"{self.operation_type}({self.operand1}, {self.operand2}) = {self.result}"
    
    def __repr__(self) -> str:

        return (
            f"Calculation(operation='{self.operation_type}', "
            f"operand1={self.operand1}, "
            f"operand2={self.operand2}, "
            f"result={self.result}, "
            f"timestamp='{self.timestamp.isoformat()}')"
        ) #pragma: no cover
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Calculation):
            return NotImplemented
        return (
            self.operation_type == other.operation_type and
            self.operand1 == other.operand1 and
            self.operand2 == other.operand2 and
            self.result == other.result
        )
    

    def format_result(self, precision: int = 10) -> str:

        try:
            # Remove trailing zeros and format to specified precision
            return str(self.result.normalize().quantize(
                Decimal('0.' + '0' * precision)
            ).normalize())
        except InvalidOperation:  # pragma: no cover
            return str(self.result)