# Importing sys module to access exception details
import sys
from src.logger import logging

# This code defines a custom exception handling mechanism that captures detailed error information including:
# File name where the error occurred, 
# Line number where the error was raised, 
# Actual error message

def error_message_detail(error, error_detail:sys):
    """It generates error message including the file name, line number, and error description"""
    _, _, exc_tb = error_detail.exc_info()      # Return tuple containing (exception_type, exception_value, traceback_object)
    # Retrieve the filename where the exception (error) occurred
    file_name = exc_tb.tb_frame.f_code.co_filename          # exc_tb 
    # Extract the line number where error was raised
    line_number = exc_tb.tb_lineno
    error_message = f"Error occurred in python script name [{file_name}] line number [{line_number}] error message [{str(error)}]"

    return error_message

class CustomException(Exception):
    """Custom exception class that extends the built-in Exception class"""
    def __init__(self, error_message, error_detail: sys):
        # Inheriting parent exception class
        super().__init__(error_message)  
        self.error_message = error_message_detail(error_message, error_detail=error_detail)

    def __str__(self):
        """Returns the formatted error message when the exception is printed."""
        return self.error_message

