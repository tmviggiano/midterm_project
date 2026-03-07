import datetime
from pathlib import Path
import pandas as pd
import pytest
from unittest.mock import MagicMock, Mock, patch, PropertyMock
from decimal import Decimal
from tempfile import TemporaryDirectory
from app.calculator import Calculator
from app.calculator_repl import calculator_repl
from app.calculator_config import CalculatorConfig
from app.exceptions import OperationError, ValidationError
from app.history import LoggingObserver, AutosaveObserver
from app.operations import OperationFactory
from app.calculator_memento import CalculatorMemento




@patch('builtins.input', side_effect=['exit'])
@patch('builtins.print')
def test_calculator_repl_exit_error(mock_print, mock_input):
    with patch('app.calculator.Calculator.save_history', side_effect=Exception) as mock_save_history:
        calculator_repl()
        mock_save_history.assert_called_once()
        mock_print.assert_any_call("Goodbye!")

@patch('builtins.input', side_effect=['exit'])
@patch('builtins.print')
def test_calculator_repl_exit(mock_print, mock_input):
    with patch('app.calculator.Calculator.save_history') as mock_save_history:
        calculator_repl()
        mock_save_history.assert_called_once()
        mock_print.assert_any_call("History saved successfully")
        mock_print.assert_any_call("Goodbye!")


@patch('builtins.input', side_effect=['help','exit'])
@patch('builtins.print')
def test_calc_help(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("\nAvailable commands:")

@patch('builtins.input', side_effect=['history','exit'])
@patch('builtins.print')
def test_calc_show_history(mock_print, mock_input):
    with patch('app.calculator.Calculator.show_history') as mock_show_history:
        calculator_repl()
        mock_show_history.assert_called_once()
        mock_print.assert_any_call("\nCalculation history:")

@patch('builtins.input', side_effect=['add', '1', '2','history', 'exit'])
@patch('builtins.print')
def test_calc_show_history_values(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("\nCalculation history:")

@patch('builtins.input', side_effect=['history', 'exit'])
@patch('builtins.print')
def test_calc_show_history_negative(mock_print, mock_input):
    with patch('app.calculator.Calculator.show_history') as mock_history:
        mock_history.return_value = None
        calculator_repl()
        mock_history.assert_called_once()
        mock_print.assert_any_call("No calculations in history!")

@patch('builtins.input', side_effect=['clear', 'exit'])
@patch('builtins.print')
def test_calc_clear_history(mock_print, mock_input):
    with patch('app.calculator.Calculator.clear_history') as mock_clear:
        mock_clear.return_value = None
        calculator_repl()
        mock_clear.assert_called_once()
        mock_print.assert_any_call("History cleared")

@patch('builtins.input', side_effect=['undo', 'exit'])
@patch('builtins.print')
def test_calc_undo(mock_print, mock_input):
    with patch('app.calculator.Calculator.undo') as mock_undo:
        mock_undo.return_value = True
        calculator_repl()
        mock_undo.assert_called_once()
        mock_print.assert_any_call("Operation undone")

@patch('builtins.input', side_effect=['undo', 'exit'])
@patch('builtins.print')
def test_calc_undo_false(mock_print, mock_input):
    with patch('app.calculator.Calculator.undo') as mock_undo:
        mock_undo.return_value = False
        calculator_repl()
        mock_undo.assert_called_once()
        mock_print.assert_any_call("Nothing to undo")

@patch('builtins.input', side_effect=['redo', 'exit'])
@patch('builtins.print')
def test_calc_redo_false(mock_print, mock_input):
    with patch('app.calculator.Calculator.redo') as mock_redo:
        mock_redo.return_value = False
        calculator_repl()
        mock_redo.assert_called_once()
        mock_print.assert_any_call("Nothing to redo")

@patch('builtins.input', side_effect=['redo', 'exit'])
@patch('builtins.print')
def test_calc_redo_true(mock_print, mock_input):
    with patch('app.calculator.Calculator.redo') as mock_redo:
        mock_redo.return_value = True
        calculator_repl()
        mock_redo.assert_called_once()
        mock_print.assert_any_call("Operation redone")

@patch('builtins.input', side_effect=['save', 'exit'])
@patch('builtins.print')
def test_calc_save_true(mock_print, mock_input):
    with patch('app.calculator.Calculator.save_history') as mock_save:
        mock_save.return_value = None
        calculator_repl()
        assert mock_save.call_count == 2
        mock_print.assert_any_call("History saved successfully")

@patch('builtins.input', side_effect=['save', 'exit'])
@patch('builtins.print')
def test_calc_save_false(mock_print, mock_input):
    with patch('app.calculator.Calculator.save_history', side_effect = Exception("Save failed")) as mock_save:
        calculator_repl()
        assert mock_save.call_count == 2
        mock_print.assert_any_call("Error saving history: Save failed")

@patch('builtins.input', side_effect=['load', 'exit'])
@patch('builtins.print')
def test_calc_load_positive(mock_print, mock_input):
    with patch('app.calculator.Calculator.load_history') as mock_load:
        calculator_repl()
        assert mock_load.call_count == 2
        mock_print.assert_any_call("History loaded successfully")

@patch('builtins.input', side_effect=['load', 'exit'])
@patch('builtins.print')
def test_calc_load_negative(mock_print, mock_input):
    with patch('app.calculator.Calculator.load_history', side_effect=Exception("Load failed")) as mock_load:
        calculator_repl()
        assert mock_load.call_count == 2
        mock_print.assert_any_call("Error loading history: Load failed")


@patch('builtins.input', side_effect=['add', 'cancel', 'exit'])
@patch('builtins.print')
def test_calc_cancel_operation_a(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("Operation cancelled")

@patch('builtins.input', side_effect=['add','2', 'cancel', 'exit'])
@patch('builtins.print')
def test_calc_cancel_operation_b(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("Operation cancelled")