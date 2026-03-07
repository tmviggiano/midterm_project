import pytest
from unittest.mock import Mock, patch
from app.calculation import Calculation
from app.history import LoggingObserver, AutosaveObserver
from app.calculator import Calculator
from app.calculator_config import CalculatorConfig


calculation_mock = Mock(spec=Calculation)
calculation_mock.operation_type = "add"
calculation_mock.operand1 = 1
calculation_mock.operand2 = 2
calculation_mock.result = 3


def test_logging_obs_no_calc():
    observer = LoggingObserver()
    with pytest.raises(AttributeError):
        observer.update(None)

@patch("logging.info")
def test_logging_obs(mock_log):
    observer = LoggingObserver()
    observer.update(calculation_mock)
    mock_log.assert_called_once_with("Calcluation performed: add (1, 2) = 3")


@patch('logging.info')
def test_autosave_obs(logging_info_mock):
    calculator_mock = Mock(spec=Calculator)
    calculator_mock.config = Mock(spec=CalculatorConfig)
    calculator_mock.config.auto_save = True
    observer = AutosaveObserver(calculator_mock)
    
    observer.update(calculation_mock)
    logging_info_mock.assert_called_once_with("History auto-saved")

def test_autosave_obs_no_config():
    with pytest.raises(TypeError):
        AutosaveObserver(None)  # Passing None should raise a TypeError

@patch('logging.info')
def test_autosave_obs_no_calc(logging_info_mock):
    calculator_mock = Mock(spec=Calculator)
    calculator_mock.config = Mock(spec=CalculatorConfig)
    calculator_mock.config.auto_save = True
    observer = AutosaveObserver(calculator_mock)
    with pytest.raises(AttributeError):
        observer.update(None)
@patch('logging.info')
def test_autosave_obs_no_auto(logging_info_mock):
    calculator_mock = Mock(spec=Calculator)
    calculator_mock.config = Mock(spec=CalculatorConfig)
    calculator_mock.config.auto_save = False
    observer = AutosaveObserver(calculator_mock)
    
    observer.update(calculation_mock)
    calculator_mock.save_history.assert_not_called()

