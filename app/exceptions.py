class CalculationError(Exception):
    """
    Calculator specifi base class for exceptions
    """
    pass

class ValidationError(CalculationError):

    """
    Raised when input validation fails
    """
    pass

class OperationError(CalculationError):

    """
    Raised when a calculation operation fails
    """
    pass

class ConfigurationError(CalculationError):

    """
    Raised when a calculator configuration error occurs
    """

    pass