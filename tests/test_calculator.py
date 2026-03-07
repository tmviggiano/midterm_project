import datetime
from pathlib import Path
import pandas as pd
import pytest
from unittest.mock import patch, PropertyMock
from decimal import Decimal
from tempfile import TemporaryDirectory
from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from app.exceptions import OperationError, ValidationError
from app.history import LoggingObserver
from app.operations import Addition


@pytest.fixture
def calculator():
    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        config = CalculatorConfig(base_dir=temp_path)

        with patch.object(CalculatorConfig, 'log_dir', new_callable=PropertyMock) as mock_log_dir, \
             patch.object(CalculatorConfig, 'log_file', new_callable=PropertyMock) as mock_log_file, \
             patch.object(CalculatorConfig, 'history_dir', new_callable=PropertyMock) as mock_history_dir, \
             patch.object(CalculatorConfig, 'history_file', new_callable=PropertyMock) as mock_history_file:
            
            mock_log_dir.return_value = temp_path / "logs"
            mock_log_file.return_value = temp_path / "logs/calculator.log"
            mock_history_dir.return_value = temp_path / "history"
            mock_history_file.return_value = temp_path / "history/calculator_history.csv"
            yield Calculator(config=config)


def test_calculator_init(calculator):
    assert calculator.history ==[]
    assert calculator.undo_stack==[]
    assert calculator.redo_stack==[]
    assert calculator.observers==[]
    assert calculator.operation_name is None
    assert calculator.operation_strategy is None


def test_add_observer(calculator):
    observer = LoggingObserver()
    calculator.add_observer(observer)
    assert observer in calculator.observers

def test_remove_observer(calculator):
    observer = LoggingObserver()
    calculator.add_observer(observer)
    calculator.remove_observer(observer)
    assert observer not in calculator.observers

@patch('app.calculator.Calculation')
@patch('app.history.LoggingObserver')
def test_notify_observers(mock_observer, mock_calculation, calculator):
    mock_calc_instance = mock_calculation.return_value
    mock_instance = mock_observer.return_value
    calculator.add_observer(mock_instance)
    calculator.notify_observers(mock_calc_instance)
    mock_instance.update.assert_called_once_with(mock_calc_instance)


def test_set_operation(calculator):
    calculator.set_operation("add")
    assert isinstance(calculator.operation_strategy, Addition)

def test_perform_operation(calculator):

    calculator.set_operation('add')
    result = calculator.perform_operation('1','2')
    assert result == 3

def test_perform_operation_no_operation(calculator):

    with pytest.raises(OperationError, match="No operation set"):
        result = calculator.perform_operation('1','2')

def test_perform_operation_history_size(calculator):

    calculator.set_operation('add')
    calculator.config.max_history_size = 1
    calculator.perform_operation('1','2')
    result = calculator.perform_operation('1','2')
    assert result == 3

def test_perform_operation_invalid1(calculator):
    calculator.set_operation('add')
    with pytest.raises(ValidationError):
        calculator.perform_operation('notaNumber','2')

def test_perform_operation_error(calculator):
    calculator.set_operation('add')
    with patch("app.operations.Addition.execute", side_effect=Exception("Boom")):
        with pytest.raises(OperationError): 
            calculator.perform_operation(2, 3)

@patch('app.calculator.pd.read_csv')
@patch('app.calculator.Path.exists', return_value=True)
def test_load_history(mock_exists, mock_read_csv, calculator):
    mock_read_csv.return_value = pd.DataFrame({
        'operation': ['add'],
        'operand1': ['1'],
        'operand2': ['2'],
        'result': ['3'],
        'timestamp': [datetime.datetime.now().isoformat()]
    })
    
    calculator.load_history()
    assert len(calculator.history) == 1
    assert calculator.history[0].operation_type == "add"
    assert calculator.history[0].operand1 == Decimal("1")
    assert calculator.history[0].operand2 == Decimal("2")
    assert calculator.history[0].result == Decimal("3")

@patch('app.calculator.pd.read_csv')
@patch('app.calculator.Path.exists', return_value=True)
def test_load_history_empty_df(mock_exists, mock_read_csv, calculator):
    mock_read_csv.return_value = pd.DataFrame()
    calculator.load_history()
    assert len(calculator.history) == 0


@patch('app.calculator.pd.DataFrame.to_csv')
def test_save_history(mock_to_csv, calculator):
    calculator.set_operation('add')
    calculator.perform_operation(2, 3)
    calculator.save_history()
    mock_to_csv.assert_called_once()

@patch('app.calculator.Path.exists', return_value=True)
def test_load_history_error(mock_exists,calculator):
    with patch("app.calculator.pd.read_csv", side_effect=Exception("Boom")):
        with pytest.raises(OperationError): 
            calculator.load_history()

@patch('app.calculator.pd.DataFrame.to_csv')
def test_save_history_empty(mock_to_csv, calculator):
    calculator.save_history()
    mock_to_csv.assert_called_once()

@patch('app.calculator.Path.exists', return_value=True)
def test_save_history_error(mock_exists, calculator):
    with patch("app.calculator.pd.DataFrame.to_csv", side_effect=Exception("Boom")):
        with pytest.raises(OperationError): 
            calculator.save_history()

def test_get_history_dataframe(calculator):
    calculator.set_operation('add')

    calculator.perform_operation(1, 2)

    df = calculator.get_history_df()

    expected_df = pd.DataFrame([{
        'operation': 'add',
        'operand1': '1',
        'operand2': '2',
        'result': '3',
        'timestamp': calculator.history[0].timestamp.isoformat()
    }])


    pd.testing.assert_frame_equal(df, expected_df)

def test_undo(calculator):
    calculator.set_operation('add')
    calculator.perform_operation(1, 2)

    result = calculator.undo()
    assert result == True

def test_undo_empty (calculator):

    result = calculator.undo()
    assert result == False

def test_redo(calculator):
    calculator.set_operation('add')
    calculator.perform_operation(1, 2)

    calculator.undo()
    result = calculator.redo()
    assert result == True

def test_redo_empty (calculator):

    result = calculator.redo()
    assert result == False

def test_clear_history(calculator):
    calculator.set_operation('add')
    calculator.perform_operation(1, 2)

    assert len(calculator.history) ==1
    calculator.clear_history()
    assert len(calculator.history) ==0

def test_show_history(calculator):
    calculator.set_operation('add')
    calculator.perform_operation(1, 2)

    result = calculator.show_history()

    expected = "add(1, 2) = 3"
    assert result[0] == expected