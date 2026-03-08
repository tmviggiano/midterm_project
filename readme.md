# Midterm Project -- Python Calculator

A modular command-line calculator implemented in Python that
demonstrates object-oriented design, design patterns, configuration
management, and automated testing.

This project was developed as part of a software engineering midterm
assignment and focuses on building a maintainable and extensible
calculator system with proper error handling and testing.

------------------------------------------------------------------------

# Features

-   Modular calculator architecture
-   Object-Oriented Design
-   Factory Pattern for creating operations
-   Command-line interaction (REPL style)
-   Operation history tracking
-   Pandas DataFrame export of history
-   Environment-based configuration
-   Comprehensive unit tests with pytest
-   Robust error handling

------------------------------------------------------------------------

## Project Structure

```
midterm_project
├── LICENSE
├── app
│   ├── __init__.py
│   ├── calculation.py
│   ├── calculator.py
│   ├── calculator_config.py
│   ├── calculator_memento.py
│   ├── calculator_repl.py
│   ├── exceptions.py
│   ├── history
│   ├── history.py
│   ├── inputvalidators.py
│   └── operations.py
├── history
│   └── calculator_history.csv
├── logs
│   └── custom_log.log
├── main.py
├── pytest.ini
├── README.md
├── requirements.txt
└── tests
    ├── __init__.py
    ├── test_calculation.py
    ├── test_calculator.py
    ├── test_config.py
    ├── test_history.py
    ├── test_operations.py
    └── test_repl.py

------------------------------------------------------------------------

# Installation

Clone the repository:

``` bash
git clone https://github.com/tmviggiano/midterm_project.git
cd midterm_project
```

Create a virtual environment:

``` bash
python -m venv venv
```

Activate the environment:

Mac/Linux

``` bash
source venv/bin/activate
```

Windows

``` bash
venv\Scripts\activate
```

Install dependencies:

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

# Configuration

The application uses environment variables for configuration.

Create a `.env` file in the root directory:

    CALCULATOR_LOG_DIR=./logs
    CALCULATOR_HISTORY_DIR=./history
    CALCULATOR_MAX_HISTORY_SIZE=100
    CALCULATOR_AUTO_SAVE=false
    CALCULATOR_BASE_DIR=.
    CALCULATOR_PRECISION=1000
    CALCULATOR_MAX_INPUT_VALUE=1e999
    CALCULATOR_DEFAULT_ENCODING=utf-8
    CALCULATOR_HISTORY_FILE=./history/calculator_history.csv
    CALCULATOR_LOG_FILE=./logs/custom_log.log

Environment variables are loaded using `python-dotenv`.

------------------------------------------------------------------------

# Usage

Run the calculator:

``` bash
python3 main.py
```

Example commands:

    add 2 3
    subtract 10 5
    multiply 4 6
    divide 20 4
    history
    undo
    redo
    save
    help
    load

Example output:

    Result: 5

------------------------------------------------------------------------

# Operation Architecture

The calculator uses the **Factory Pattern** to dynamically create
operation objects.

Example workflow:

1.  User selects an operation
2.  `OperationFactory` instantiates the correct operation class
3.  Operation executes calculation
4.  Result is stored in calculator history

------------------------------------------------------------------------

# Testing

Tests are written using **pytest**.

Run tests:

``` bash
pytest
```

Example test coverage includes:

-   Calculator operations
-   Operation factory
-   Error handling
-   DataFrame history export

------------------------------------------------------------------------

# Example History Output

The calculator tracks operations and can export them as a Pandas
DataFrame:

  operation   operand1   operand2   result   timestamp
  ----------- ---------- ---------- -------- ------------
  add         1          2          3        2026-03-01

------------------------------------------------------------------------

# Technologies Used

-   Python
-   pytest
-   pandas
-   python-dotenv
-   dataclasses
-   decimal module

------------------------------------------------------------------------

# Design Patterns

This project demonstrates the following patterns:

**Factory Pattern**\
Used to dynamically instantiate operation classes.

**Decorator Pattern**\
Used to dynamically populate the available operations for the operation factory operation classes.

**Separation of Concerns**\
Calculator logic, operations, configuration, and tests are separated
into modules.

------------------------------------------------------------------------

# New features

**save function**\
Saves the history of calculations to a csv using pandas

**undo function**\
removes the most recent calculation from the history using a memento observer

**redo function**\
re-adds the most recent calculation to the history using a memento observer

**clear function**\
deletes all contents in the history

**load function**\
populates history using data stored in the csv file


# Author

Tom Viggiano

GitHub:\
https://github.com/tmviggiano
