from unittest.mock import MagicMock, Mock, patch, PropertyMock
from app.calculator_repl import calculator_repl
from app.exceptions import ValidationError
import re

def strip_ansi(text):
    ansi_escape =re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)




@patch('builtins.input', side_effect=['exit'])
@patch('builtins.print')
def test_calculator_repl_exit_error(mock_print, mock_input):
    with patch('app.calculator.Calculator.save_history', side_effect=Exception) as mock_save_history:
        calculator_repl()
        mock_save_history.assert_called_once()
        printed = [strip_ansi(call.args[0]) for call in mock_print.call_args_list]

        assert "Goodbye!" in printed

@patch('builtins.input', side_effect=['exit'])
@patch('builtins.print')
def test_calculator_repl_exit(mock_print, mock_input):
    with patch('app.calculator.Calculator.save_history') as mock_save_history:
        calculator_repl()
        mock_save_history.assert_called_once()
        printed = [strip_ansi(call.args[0]) for call in mock_print.call_args_list]

        assert "History saved successfully" in printed
        assert "Goodbye!" in printed


@patch('builtins.input', side_effect=['help','exit'])
@patch('builtins.print')
def test_calc_help(mock_print, mock_input):
    calculator_repl()
    printed = [strip_ansi(call.args[0]) for call in mock_print.call_args_list]
    assert "\nAvailable commands:" in printed

@patch('builtins.input', side_effect=['history','exit'])
@patch('builtins.print')
def test_calc_show_history(mock_print, mock_input):
    with patch('app.calculator.Calculator.show_history') as mock_show_history:
        calculator_repl()
        mock_show_history.assert_called_once()
        printed = [strip_ansi(call.args[0]) for call in mock_print.call_args_list]
        assert "\nCalculation history:" in printed

@patch('builtins.input', side_effect=['add', '1', '2','history', 'exit'])
@patch('builtins.print')
def test_calc_show_history_values(mock_print, mock_input):
    calculator_repl()
    printed = [strip_ansi(call.args[0]) for call in mock_print.call_args_list]
    assert "\nCalculation history:" in printed

@patch('builtins.input', side_effect=['history', 'exit'])
@patch('builtins.print')
def test_calc_show_history_negative(mock_print, mock_input):
    with patch('app.calculator.Calculator.show_history') as mock_history:
        mock_history.return_value = None
        calculator_repl()
        mock_history.assert_called_once()
        printed = [strip_ansi(call.args[0]) for call in mock_print.call_args_list]
        assert "No calculations in history!" in printed

@patch('builtins.input', side_effect=['clear', 'exit'])
@patch('builtins.print')
def test_calc_clear_history(mock_print, mock_input):
    with patch('app.calculator.Calculator.clear_history') as mock_clear:
        mock_clear.return_value = None
        calculator_repl()
        mock_clear.assert_called_once()
        printed = [strip_ansi(call.args[0]) for call in mock_print.call_args_list]
        assert "History cleared" in printed

@patch('builtins.input', side_effect=['undo', 'exit'])
@patch('builtins.print')
def test_calc_undo(mock_print, mock_input):
    with patch('app.calculator.Calculator.undo') as mock_undo:
        mock_undo.return_value = True
        calculator_repl()
        mock_undo.assert_called_once()
        printed = [strip_ansi(call.args[0]) for call in mock_print.call_args_list]
        assert "Operation undone" in printed

@patch('builtins.input', side_effect=['undo', 'exit'])
@patch('builtins.print')
def test_calc_undo_false(mock_print, mock_input):
    with patch('app.calculator.Calculator.undo') as mock_undo:
        mock_undo.return_value = False
        calculator_repl()
        mock_undo.assert_called_once()
        printed = [strip_ansi(call.args[0]) for call in mock_print.call_args_list]
        assert "Nothing to undo" in printed

@patch('builtins.input', side_effect=['redo', 'exit'])
@patch('builtins.print')
def test_calc_redo_false(mock_print, mock_input):
    with patch('app.calculator.Calculator.redo') as mock_redo:
        mock_redo.return_value = False
        calculator_repl()
        mock_redo.assert_called_once()
        printed = [strip_ansi(call.args[0]) for call in mock_print.call_args_list]
        assert "Nothing to redo" in printed

@patch('builtins.input', side_effect=['redo', 'exit'])
@patch('builtins.print')
def test_calc_redo_true(mock_print, mock_input):
    with patch('app.calculator.Calculator.redo') as mock_redo:
        mock_redo.return_value = True
        calculator_repl()
        mock_redo.assert_called_once()
        printed = [strip_ansi(call.args[0]) for call in mock_print.call_args_list]
        assert "Operation redone" in printed

@patch('builtins.input', side_effect=['save', 'exit'])
@patch('builtins.print')
def test_calc_save_true(mock_print, mock_input):
    with patch('app.calculator.Calculator.save_history') as mock_save:
        mock_save.return_value = None
        calculator_repl()
        assert mock_save.call_count == 2
        printed = [strip_ansi(call.args[0]) for call in mock_print.call_args_list]
        assert "History saved successfully" in printed

@patch('builtins.input', side_effect=['save', 'exit'])
@patch('builtins.print')
def test_calc_save_false(mock_print, mock_input):
    with patch('app.calculator.Calculator.save_history', side_effect = Exception("Save failed")) as mock_save:
        calculator_repl()
        assert mock_save.call_count == 2
        printed = [strip_ansi(call.args[0]) for call in mock_print.call_args_list]
        assert "Error saving history: Save failed" in printed

@patch('builtins.input', side_effect=['load', 'exit'])
@patch('builtins.print')
def test_calc_load_positive(mock_print, mock_input):
    with patch('app.calculator.Calculator.load_history') as mock_load:
        calculator_repl()
        assert mock_load.call_count == 2
        printed = [strip_ansi(call.args[0]) for call in mock_print.call_args_list]
        assert "History loaded successfully" in printed

@patch('builtins.input', side_effect=['load', 'exit'])
@patch('builtins.print')
def test_calc_load_negative(mock_print, mock_input):
    with patch('app.calculator.Calculator.load_history', side_effect=Exception("Load failed")) as mock_load:
        calculator_repl()
        assert mock_load.call_count == 2
        printed = [strip_ansi(call.args[0]) for call in mock_print.call_args_list]
        assert "Error loading history: Load failed" in printed


@patch('builtins.input', side_effect=['add', 'cancel', 'exit'])
@patch('builtins.print')
def test_calc_cancel_operation_a(mock_print, mock_input):
    calculator_repl()
    printed = [strip_ansi(call.args[0]) for call in mock_print.call_args_list]
    assert "Operation cancelled" in printed

@patch('builtins.input', side_effect=['add','2', 'cancel', 'exit'])
@patch('builtins.print')
def test_calc_cancel_operation_b(mock_print, mock_input):
    calculator_repl()
    printed = [strip_ansi(call.args[0]) for call in mock_print.call_args_list]
    assert "Operation cancelled" in printed


@patch('builtins.input', side_effect=['unknown', 'cancel', 'exit'])
@patch('builtins.print')
def test_calc_unknown_command(mock_print, mock_input):
    calculator_repl()
    printed = [strip_ansi(call.args[0]) for call in mock_print.call_args_list]
    assert "Unknown command: 'unknown'. Type 'help' for list of available commands" in printed

@patch('builtins.input', side_effect=['add', '2', '3', 'exit'])
@patch('builtins.print')
def test_calc_unexpected_error(mock_print, mock_input):

    with patch('app.calculator.Calculator.perform_operation', side_effect=Exception("unexpected")):
        with patch('app.calculator.Calculator.set_operation'):
            calculator_repl()
    printed = [strip_ansi(call.args[0]) for call in mock_print.call_args_list]
    assert "Unexpected error: unexpected" in printed

@patch('builtins.input', side_effect=['add', '2', '3', 'exit'])
@patch('builtins.print')
def test_calc_validation_error(mock_print, mock_input):

    with patch('app.calculator.Calculator.perform_operation', side_effect=ValidationError("unexpected")):
        with patch('app.calculator.Calculator.set_operation'):
            calculator_repl()
    printed = [strip_ansi(call.args[0]) for call in mock_print.call_args_list]
    assert "Error: unexpected" in printed

@patch('builtins.input', side_effect=EOFError)
@patch('builtins.print')
def test_eof_error(mock_print, mock_input):
    calculator_repl()
    printed = [strip_ansi(call.args[0]) for call in mock_print.call_args_list]
    assert "\nInput terminated. Exiting..." in printed


@patch('builtins.input', side_effect=[KeyboardInterrupt, 'exit'])
@patch('builtins.print')
def test_keyboard_interrupt_error(mock_print, mock_input):
    calculator_repl()
    printed = [strip_ansi(call.args[0]) for call in mock_print.call_args_list]
    assert "\nOperation cancelled" in printed