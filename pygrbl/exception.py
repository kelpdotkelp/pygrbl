"""
Part of pygrbl

Noah Stieler, 2023
"""


class PyGRBLException(Exception):
    pass


class ChamberNotDefinedException(PyGRBLException):
    """Raised when _chamber in main has not been set."""
    pass


class PointOutOfBoundsException(PyGRBLException):
    """Raised when PyGRBLMachine attempts to move or has moved out of bounds."""
    pass


class OriginNotSetException(PyGRBLException):
    """Raised when attempting to change position before setting origin."""
    pass


class CommandException(PyGRBLException):
    """Raised when grbl sends an error."""

    def __init__(self, cmd: str = ''):
        self.cmd = cmd


class CSVLoadException(PyGRBLException):
    """Raised when there is a problem loading a .csv"""
    pass
