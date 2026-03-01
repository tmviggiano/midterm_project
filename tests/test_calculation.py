import pytest
from unittest.mock import MagicMock
from decimal import Decimal
from datetime import datetime
from app.calculation import Calculation
from app.exceptions import OperationError, ValidationError
import logging


def test_addition():
    calc = Calculation(operation_type="add", operand1=Decimal("2"), operand2=Decimal("3"))
    assert calc.result == Decimal("5")

def test_unknown_op():
    with pytest.raises(OperationError):
        calc = Calculation("unknown", Decimal("1"), Decimal("2"))
        
def test_calculation_error():
    calc = Calculation("add", Decimal("1"), Decimal("1"))

    # Replace operation with mock
    calc.op = MagicMock()
    calc.op.execute.side_effect = ValueError("Boom")

    with pytest.raises(OperationError, match="Operation failed: Boom"):
        calc.calculate()
def test_from_dict():
    data = {
        "operation": "add",
        "operand1": "3",
        "operand2": "4",
        "result": "7",
        "timestamp": datetime.now().isoformat()
    }
    calc = Calculation.from_dict(data)
    assert calc.operation_type == "add"
    assert calc.operand1 == Decimal("3")
    assert calc.operand2 == Decimal("4")
    assert calc.result == Decimal("7")

def test_invalid_from_dict():
    data = {
        "operation": "add",
        "operand1": "invalid",
        "operand2": "3",
        "result": "9",
        "timestamp": datetime.now().isoformat()
    }
    with pytest.raises(OperationError):
        Calculation.from_dict(data)

def test_to_dict():
    calc = Calculation(operation_type="add", operand1=Decimal("4"), operand2=Decimal("3"))
    result_dict = calc.to_dict()
    assert result_dict == {
        "operation": "add",
        "operand1": "4",
        "operand2": "3",
        "result": "7",
        "timestamp": calc.timestamp.isoformat()
    }

def test_to_string():
    calc = Calculation(operation_type="add", operand1=Decimal("2"), operand2=Decimal("3"))
    assert str(calc) == "add(2, 3) = 5"

def test_eq():
    calc1 = Calculation(operation_type="add", operand1=Decimal("2"), operand2=Decimal("3"))
    calc2 = Calculation(operation_type="add", operand1=Decimal("2"), operand2=Decimal("3"))
    calc3 = Calculation(operation_type="subtract", operand1=Decimal("5"), operand2=Decimal("3"))
    assert calc1 == calc2
    assert calc1 != calc3
    assert (calc1 == "not a calc") is False

def test_format():
    calc = Calculation(operation_type="divide", operand1=Decimal("2"), operand2=Decimal("3"))
    assert calc.format_result(precision=2) == "0.67"
    assert calc.format_result(precision=4) == "0.6667"