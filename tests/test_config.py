import pytest
import os
from decimal import Decimal
from pathlib import Path
from app.calculator_config import CalculatorConfig
from app.exceptions import ConfigurationError


os.environ['CALCULATOR_MAX_HISTORY_SIZE'] = '100'
os.environ['CALCULATOR_AUTO_SAVE'] = 'false'
os.environ['CALCULATOR_PRECISION'] = '5'
os.environ['CALCULATOR_MAX_INPUT_VALUE'] = '100'
os.environ['CALCULATOR_DEFAULT_ENCODING'] = 'utf-8'
os.environ['CALCULATOR_LOG_DIR'] = './test_logs'
os.environ['CALCULATOR_HISTORY_DIR'] = './test_history'
os.environ['CALCULATOR_HISTORY_FILE'] = './test_history/test_history.csv'
os.environ['CALCULATOR_LOG_FILE'] = './test_logs/test_log.log'

def clear_env_vars(*args):
    for var in args:
        os.environ.pop(var, None)


def test_default_configs():
    config = CalculatorConfig()
    assert config.max_history_size == 100
    assert config.auto_save is False
    assert config.precision == 5
    assert config.max_input_value == Decimal("100")
    assert config.default_encoding == 'utf-8'
    assert config.log_dir == Path('./test_logs').resolve()
    assert config.history_dir == Path('./test_history').resolve()
    assert config.history_file == Path('./test_history/test_history.csv').resolve()
    assert config.log_file == Path('./test_logs/test_log.log').resolve()

def test_custom_configs():
    config = CalculatorConfig(
        max_history_size=400,
        auto_save=True,
        precision=10,
        max_input_value= Decimal('10000'),
        default_encoding='utf-8'
    )
    config.validate()
    assert config.max_history_size == 400
    assert config.auto_save is True
    assert config.precision == 10
    assert config.max_input_value == Decimal("10000")
    assert config.default_encoding == 'utf-8'

def test_invalid_max_history_size():
    with pytest.raises(ConfigurationError, match="Config: max_history_size - must be a positive value"):
        config = CalculatorConfig(max_history_size=-1)
        config.validate()

def test_invalid_precision():
    with pytest.raises(ConfigurationError, match="Config: precision - must be a positive"):
        config = CalculatorConfig(precision=-1)
        config.validate()

def test_invalid_max_input_value():
    with pytest.raises(ConfigurationError, match="Config: max_input_value - must be positive"):
        config = CalculatorConfig(max_input_value=Decimal("-1"))
        config.validate()
